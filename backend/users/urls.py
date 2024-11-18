from django.urls import path
from .views.user_signup import email_password_signup, google_signup
from .views.user_profile import update_user_profile


urlpatterns = [
    path('signup/email-password/', email_password_signup, name='email-password-signup'),    # メール&パスワードでのサインアップ
    path('signup/google/', google_signup, name='google-signup'),                            # Google認証でのサインアップ
    path('user-profile/', update_user_profile, name='user-profile'),                        # ユーザープロフィールの更新
]