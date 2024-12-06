from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import Like, Message, CustomUser
from django.utils.timezone import now

# 統一レスポンスフォーマット
def success_response(data, message="Success", status_code=200):
    return Response({"status": "success", "message": message, "data": data}, status=status_code)

def error_response(error, status_code=400):
    return Response({"status": "error", "message": error}, status=status_code)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 認証が必要
def get_matched_users(request):
    """
    マッチングが成立したユーザー一覧を取得するAPI
    """
    user = request.user

    # マッチング一覧を取得
    matches = Like.objects.filter(
        Q(sender=user, is_matched=True) | Q(receiver=user, is_matched=True)
    ).select_related('sender', 'receiver')

    data = []
    for match in matches:
        matched_user = match.receiver if match.sender == user else match.sender
        data.append({
            "user_id": str(matched_user.user_id),
            "user_name": matched_user.profile.user_name if hasattr(matched_user, 'profile') else None,
            "profile_image": matched_user.profile.profile_image.url if hasattr(matched_user, 'profile') and matched_user.profile.profile_image else None,
            "matched_at": match.created_at
        })

    return success_response(data, "マッチングユーザー一覧を取得しました。")


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 認証が必要
def get_messages(request):
    """
    特定のユーザーとのDM履歴を取得するAPI
    """
    sender = request.user
    receiver_id = request.GET.get('receiver_id')
    limit = int(request.GET.get('limit', 50))

    if not receiver_id:
        return error_response("receiver_id は必須です。", 400)

    receiver = get_object_or_404(CustomUser, user_id=receiver_id)

    # マッチング確認
    if not Like.objects.filter(
        Q(sender=sender, receiver=receiver, is_matched=True) |
        Q(sender=receiver, receiver=sender, is_matched=True)
    ).exists():
        return error_response("マッチングが成立していないユーザーです。", 403)

    # メッセージ履歴を取得
    messages = Message.objects.filter(
        Q(sender=sender, receiver=receiver) |
        Q(sender=receiver, receiver=sender)
    ).order_by('-created_at')[:limit]

    data = [
        {
            "sender_id": str(message.sender.user_id),
            "receiver_id": str(message.receiver.user_id),
            "content": message.content,
            "created_at": message.created_at,
            "is_read": message.is_read
        }
        for message in messages
    ]

    return success_response(data, "メッセージ履歴を取得しました。")


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 認証が必要
def send_message(request):
    """
    特定のユーザーにメッセージを送信するAPI
    """
    sender = request.user
    receiver_id = request.data.get('receiver_id')
    content = request.data.get('content')

    if not receiver_id or not content:
        return error_response("receiver_id と content は必須です。", 400)

    receiver = get_object_or_404(CustomUser, user_id=receiver_id)

    # マッチング確認
    if not Like.objects.filter(
        Q(sender=sender, receiver=receiver, is_matched=True) |
        Q(sender=receiver, receiver=sender, is_matched=True)
    ).exists():
        return error_response("マッチングが成立していないユーザーです。", 403)

    # メッセージを保存
    message = Message.objects.create(sender=sender, receiver=receiver, content=content, created_at=now())

    return success_response({
        "sender_id": str(message.sender.user_id),
        "receiver_id": str(message.receiver.user_id),
        "content": message.content,
        "created_at": message.created_at
    }, "メッセージを送信しました。", 201)
