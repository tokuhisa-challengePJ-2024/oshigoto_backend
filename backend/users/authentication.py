from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import firebase_admin
from firebase_admin import auth

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Authorization ヘッダーからトークンを取得
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split(' ')[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')
            return (self.get_user(uid), None)
        except Exception as e:
            raise AuthenticationFailed('Invalid Firebase token')

    def get_user(self, uid):
        # Firebase UID からユーザーを取得（DBに保存されたカスタムユーザーを検索）
        from users.models import CustomUser
        try:
            user = CustomUser.objects.get(fa_id=uid)
            return user
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('No such user')

    def authenticate_header(self, request):
        # 必要に応じて認証スキームのヘッダー情報を返す
        return 'Bearer'
