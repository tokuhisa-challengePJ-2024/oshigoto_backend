from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Profile  # Profile モデルをインポート
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])  # 認証不要でアクセス可能
def login_user(request):
    """
    ログインAPI: メールアドレスとパスワードでユーザーを認証し、JWTトークンを返す。
    """
    email = request.data.get("email")
    password = request.data.get("password")

    # 入力データの検証
    if not email or not password:
        return Response(
            {"error": "メールアドレスとパスワードは必須です。"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 認証
    user = authenticate(email=email, password=password)
    if user is None:
        logger.warning(f"ログイン失敗: email={email}")
        return Response(
            {"error": "メールアドレスまたはパスワードが正しくありません。"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # トークンの生成
    refresh = RefreshToken.for_user(user)
    logger.info(f"ログイン成功: email={email}")

    # プロフィール情報の取得
    try:
        profile = Profile.objects.get(user=user)  # プロフィールを取得
        profile_created_at = profile.created_at  # プロフィール作成日時
    except Profile.DoesNotExist:
        profile_created_at = None  # プロフィールがない場合は None にする

    return Response({
        "message": "ログイン成功",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "profile_created_at": profile_created_at,  # プロフィール作成日時を追加
    }, status=status.HTTP_200_OK)
