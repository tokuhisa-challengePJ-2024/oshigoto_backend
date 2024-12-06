from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.login import login_user
from .views.user_signup import email_password_signup, google_signup
from .views.user_role import assign_role  # 役割登録用APIをインポート
from .views.user_profile import update_user_profile
from .views.get_user_profile import get_user_profile
from .views.get_user_list import get_user_list
from .views.matching import send_like, get_likes, check_match, approve_like
from .views.dm import get_matched_users, get_messages, send_message

urlpatterns = [
    # ログイン・サインアップ機能
    path('login/', login_user, name='login'),                                               # ログインエンドポイント
    path('signup/email-password/', email_password_signup, name='email-password-signup'),    # メール&パスワードでのサインアップ
    path('signup/google/', google_signup, name='google-signup'),                            # Google認証でのサインアップ
    path('assign-role/', assign_role, name='assign-role'),                                  # ユーザーロールの設定
    path('user-profile/', update_user_profile, name='user-profile'),                        # ユーザープロフィールの更新
    # トークン
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),                # トークン発行エンドポイント
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),               # トークンリフレッシュエンドポイント
    # ユーザープロフィール
    path('get-profile/', get_user_profile, name='get-profile'),                             # ユーザープロフィール返答
    path('get-user-list/', get_user_list, name='get-user-list'),                            # ユーザーリスト取得
    # いいね機能
    path('send-like/', send_like, name='send-like'),                                        # いいね送信
    path('get-likes/', get_likes, name='get-likes'),                                        # いいね取得
    path('approve-like/', approve_like, name='approve-like'),                               # いいね承認
    path('check-match/', check_match, name='check-match'),                                  # マッチング成立確認
    # DM機能
    path('dm/matched-users/', get_matched_users, name='get_matched_users'),                 # マッチしたユーザー一覧
    path('dm/messages/', get_messages, name='get_messages'),                                # メッセージ履歴取得
    path('dm/send/', send_message, name='send_message'),                                    # メッセージ送信
]