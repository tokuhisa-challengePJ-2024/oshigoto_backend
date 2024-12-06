from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from ..models import Profile, CustomUser
from ..serializers import ProfileSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])  # 認証不要でアクセス可能
def get_user_profile(request):
    """
    メールアドレスとパスワードを使用してプロフィールを取得するAPI。
    未登録の場合はNULLを返す。
    """
    try:
        # リクエストからメールアドレスとパスワードを取得
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "メールアドレスとパスワードは必須です。"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ユーザーを認証
        user = authenticate(email=email, password=password)
        if not user:
            logger.warning("認証失敗: email=%s", email)
            return Response(
                {"error": "メールアドレスまたはパスワードが正しくありません。"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # プロフィールを取得
        try:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            logger.info("プロフィールが未登録のユーザー: email=%s", email)
            # NULLを返す
            return Response(
                {"profile": None},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        logger.error("プロフィール取得中にエラー発生: %s", str(e), exc_info=True)
        return Response({"error": "内部エラーが発生しました。"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)