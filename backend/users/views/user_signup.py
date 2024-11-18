# サインアップ用のエンドポイントの作成

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth as firebase_auth
from ..serializers import UserSignupSerializer
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])  # 認証なしでアクセスを許可
def email_password_signup(request):
    """
    メールアドレスとパスワードで新規ユーザーを作成するエンドポイント。
    同じメールアドレスが登録済みの場合はエラーを返す。
    """
    serializer = UserSignupSerializer(data=request.data)  # リクエストデータをシリアライズ

    # バリデーションチェック
    if serializer.is_valid():
        email = serializer.validated_data.get("email")  # リクエストデータからメールアドレスを取得

        # 同じメールアドレスがすでに存在するか確認
        if User.objects.filter(email=email).exists():
            logger.warning(f"登録済みのメールアドレスでサインアップを試みました: {email}")
            return Response(
                {"error": "このアカウントは登録済みです。"},  # エラーメッセージを返す
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user = serializer.save()  # ユーザーを保存
        logger.info(f"新しいユーザーが作成されました: {user.email}")

        return Response(
            {
                "message": "ユーザー登録が成功しました！", 
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    # バリデーションエラーの場合
    logger.error(f"ユーザー登録に失敗しました: {serializer.errors}")
    return Response(
        {
            "error": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([AllowAny])  # 認証なしでアクセスを許可
def google_signup(request):
    """
    Google認証トークンを使用して新規ユーザーを作成するエンドポイント
    """
    firebase_token = request.data.get('firebase_token')

    if not firebase_token:
        return Response(
            {"error": "Firebaseトークンが必要です"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Firebaseトークンを検証
        decoded_token = firebase_auth.verify_id_token(firebase_token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")

        if not email:
            return Response(
                {"error": "トークンからメールアドレスが取得できませんでした"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Djangoのデータベースに保存
        user, created = User.objects.get_or_create(email=email, defaults={"username": email.split("@")[0], "fa_id": uid})

        if created:
            logger.info(f"Googleユーザーが新規登録されました: {email}")
            return Response(
                {"message": "Googleユーザー登録が成功しました！", "user": {"email": email}},
                status=status.HTTP_201_CREATED
            )
        else:
            logger.info(f"既存のGoogleユーザーがログインしました: {email}")
            return Response(
                {"message": "既存のGoogleユーザーです", "user": {"email": email}},
                status=status.HTTP_200_OK
            )
    except Exception as e:
        logger.error(f"Google認証中にエラーが発生しました: {str(e)}")
        return Response(
            {"error": "Google認証中にエラーが発生しました"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
