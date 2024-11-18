# from rest_framework.viewsets import ModelViewSet  # 必要なインポートを追加
# from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth import authenticate
# from django.http import JsonResponse
# from rest_framework.views import status
# from .models import CustomUser
# from .serializers import CustomUserSerializer
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt

# class CustomUserViewSet(ModelViewSet):  # このクラスで ModelViewSet を使用
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

# # 既存のプログラムに追記です
# @api_view(['POST'])
# @permission_classes([AllowAny])  # 追加: 認証なしでアクセスを許可
# def login_view(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     if not email or not password:
#         return JsonResponse(
#             {'error': 'メールアドレスとパスワードを入力してください'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # ユーザー認証
#     user = authenticate(username=email, password=password)
#     if user is not None:
#         # 認証成功
#         return JsonResponse(
#             {'message': 'login seccess', 'username': user.username},
#             status=status.HTTP_200_OK
#         )
#     else:
#         # 認証失敗
#         return JsonResponse(
#             {'error': '認証に失敗しました。メールアドレスまたはパスワードが正しくありません'},
#             status=status.HTTP_401_UNAUTHORIZED
#         )


# @csrf_exempt  # CSRF チェックを無効化
# @api_view(['POST'])
# @permission_classes([AllowAny])  # すべてのリクエストを許可
# def firebase_login(request):
#     uid = request.data.get('fa_id')
#     email = request.data.get('email')
#     name = request.data.get('name')

#     if not uid or not email:
#         return Response({"error": "UID とメールアドレスが必要です"}, status=status.HTTP_400_BAD_REQUEST)

#     # Firebase ユーザーを Django データベースに保存
#     user, created = CustomUser.objects.get_or_create(uid=uid, defaults={"email": email, "username": name})
#     return Response({"message": "Firebase ユーザーが同期されました", "username": user.username}, status=status.HTTP_200_OK)