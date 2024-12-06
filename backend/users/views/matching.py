from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Like, CustomUser
import logging

logger = logging.getLogger(__name__)

# 統一レスポンスフォーマット
def success_response(data, message="Success", status_code=200):
    return Response({"status": "success", "message": message, "data": data}, status=status_code)

def error_response(error, status_code=400):
    return Response({"status": "error", "message": error}, status=status_code)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 認証が必要
def send_like(request):
    """
    特定のユーザーにいいねを送信するAPI
    """
    sender = request.user
    receiver_id = request.data.get('receiver_id')

    if not receiver_id:
        return error_response("receiver_id が必要です", 400)

    try:
        receiver = CustomUser.objects.get(user_id=receiver_id)

        # 既にいいね済みか確認
        if Like.objects.filter(sender=sender, receiver=receiver).exists():
            return error_response("既にいいねを送信しています", 400)

        # いいねを作成
        Like.objects.create(sender=sender, receiver=receiver)
        logger.info(f"いいね送信: {sender.email} -> {receiver.email}")
        return success_response(None, "いいねを送信しました", 201)

    except CustomUser.DoesNotExist:
        return error_response("指定されたユーザーが存在しません", 404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_likes(request):
    """
    送信済み・受信済みのいいねを取得するAPI
    """
    user = request.user
    sent_likes = Like.objects.filter(sender=user).select_related('receiver').values(
        'receiver__user_id', 'receiver__email', 'receiver__username', 'created_at'
    )
    received_likes = Like.objects.filter(receiver=user).select_related('sender').values(
        'sender__user_id', 'sender__email', 'sender__username', 'created_at'
    )

    return success_response({
        "sent_likes": list(sent_likes),
        "received_likes": list(received_likes),
    }, "いいね情報を取得しました")


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 認証が必要
def approve_like(request):
    """
    いいねを承認するAPI
    """
    sender_id = request.data.get('sender_id')  # 承認する相手のUUID
    receiver = request.user  # ログイン中のユーザー

    if not sender_id:
        return error_response("sender_id が必要です", 400)

    try:
        # sender_id に基づいて送信者を取得
        sender = get_object_or_404(CustomUser, user_id=sender_id)

        # いいねレコードを取得
        like = Like.objects.filter(sender=sender, receiver=receiver).first()

        if not like:
            return error_response("いいねが見つかりません", 404)

        # 承認処理
        like.is_matched = True
        like.save()

        # 双方向マッチングを確認
        reverse_like = Like.objects.filter(sender=receiver, receiver=sender, is_matched=True).exists()

        if reverse_like:
            logger.info(f"マッチング成立: {sender.email} <-> {receiver.email}")
            return success_response({"is_matched": True}, "マッチングが成立しました", 200)
        else:
            return success_response({"is_matched": False}, "いいねが承認されました", 200)

    except Exception as e:
        logger.error(f"いいね承認中にエラーが発生しました: {str(e)}")
        return error_response("内部エラーが発生しました", 500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 認証が必要
def check_match(request):
    """
    マッチング成立を確認するAPI
    """
    user = request.user
    matches = Like.objects.filter(
        sender=user,
        receiver__likes_received__sender=user,
        is_matched=True
    ).values(
        'receiver__user_id', 'receiver__email', 'receiver__username', 'created_at'
    )

    return success_response({"matches": list(matches)}, "マッチング情報を取得しました")
