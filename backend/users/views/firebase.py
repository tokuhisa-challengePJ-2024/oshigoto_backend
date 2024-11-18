from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth as firebase_auth
from django.contrib.auth import get_user_model
from ..models import CustomUser
import logging


User = get_user_model()
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def firebase_login(request):
    """
    Firebaseから送信されたユーザー情報を受け取り、Djangoのユーザーとして登録する
    """
    try:
        data = request.data
        fa_id = data.get('fa_id')
        email = data.get('email')
        name = data.get('name')

        if not fa_id or not email:
            return Response({"error": "fa_idとemailは必須です"}, status=status.HTTP_400_BAD_REQUEST)

        # ユーザーを作成または取得
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'fa_id': fa_id,
                'username': name or "匿名ユーザー",
            }
        )
        logger.info(f"ユーザー登録の結果: {'新規作成' if created else '既存ユーザー'}")

        return Response({
            "message": "ユーザーが正常に登録されました" if created else "既存のユーザーです",
            "user": {
                "email": user.email,
                "username": user.username,
            },
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"エラー発生: {str(e)}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
