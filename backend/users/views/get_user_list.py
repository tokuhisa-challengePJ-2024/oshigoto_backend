from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import UserRole, Profile
from ..serializers import ProfileDataSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])  # 認証なしでアクセス可能
def get_user_list(request):
    """
    登録されているユーザーリストを取得するAPI
    """
    try:
        # クエリパラメータから limit を取得
        limit = request.GET.get('limit', 10)  # デフォルトは 10
        try:
            limit = int(limit)  # limit を整数に変換
        except ValueError:
            limit = 10  # 無効な値が渡された場合はデフォルト値を使用

        # ユーザーリストを取得
        users = User.objects.all()[:limit]  # limit 件数で切り取る
        user_data = []

        for user in users:
            # UUID形式のuser_idを取得
            user_id = str(user.user_id)  # UUID を文字列として取得
            
            # ユーザーの役割を取得
            roles = list(UserRole.objects.filter(user=user).values('role'))

            # プロフィール情報を取得
            profile_instance = Profile.objects.filter(user=user).first()
            profile_data = ProfileDataSerializer(profile_instance).data if profile_instance else None

            # ユーザー情報をまとめる
            user_data.append({
                'user_id': user_id,  # UUID を設定
                'email': user.email,
                'roles': roles,
                'profile': profile_data
            })

        return Response(user_data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
