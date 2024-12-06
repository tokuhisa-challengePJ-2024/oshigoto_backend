from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser, UserRole

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 認証が必要
def assign_role(request):
    """
    ユーザーに役割を割り当てるAPI
    """
    user = request.user  # 現在のリクエストユーザー
    role = request.data.get('role')  # クライアントから送られた「役割」

    # 役割が正しいかチェック
    valid_roles = ['artist', 'creator', 'admin']
    if role not in valid_roles:
        return Response(
            {"error": f"無効な役割です。有効な役割: {', '.join(valid_roles)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # 既存の役割がある場合は更新、なければ作成
        user_role, created = UserRole.objects.get_or_create(user=user)
        user_role.role = role
        user_role.save()

        message = "役割が正常に登録されました。" if created else "役割が正常に更新されました。"
        return Response(
            {
                "message": message,
                "user": user.email,
                "role": user_role.role,
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": f"役割の登録中にエラーが発生しました: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
