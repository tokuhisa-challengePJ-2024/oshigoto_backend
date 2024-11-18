from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import auth as firebase_auth
from ..models import UserProfile, CustomUser  # 必要なモデルをインポート
import logging

logger = logging.getLogger(__name__)

class FirebaseAuthentication:
    """Firebaseトークンの認証クラス"""
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split("Bearer ")[1]

        try:
            decoded_token = firebase_auth.verify_id_token(token)
            uid = decoded_token["uid"]

            # Firebase UIDに基づいてユーザーを取得
            user = CustomUser.objects.get(fa_id=uid)
            return (user, None)
        except CustomUser.DoesNotExist:
            logger.error("ユーザーが存在しません: UID=%s", uid)
            return None
        except Exception as e:
            logger.error("Firebaseトークンの検証エラー: %s", str(e))
            return None

    def authenticate_header(self, request):
        """DRFに要求される認証ヘッダー"""
        return "Bearer"

@csrf_exempt
@api_view(['POST'])
@authentication_classes([FirebaseAuthentication])  # Firebaseトークンを検証
@permission_classes([IsAuthenticated])  # 認証されたユーザーのみ許可
def update_user_profile(request):
    """
    ユーザープロファイルを作成または更新するAPI
    """
    try:
        logger.info("受信したリクエストデータ: %s", request.data)

        user = request.user  # 認証されたユーザー
        user_type = request.data.get('user_type')

        if not user_type:
            logger.error("user_type が指定されていません")
            return Response({"error": "user_type が指定されていません"}, status=status.HTTP_400_BAD_REQUEST)

        # UserProfile を作成または更新
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'user_type': user_type}
        )
        if not created:
            profile.user_type = user_type
            profile.save()

        logger.info("ユーザープロファイルの登録成功: %s", profile)

        return Response({
            "message": "ユーザープロファイルが正常に登録されました",
            "user_type": profile.user_type,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error("エラー発生: %s", str(e), exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)