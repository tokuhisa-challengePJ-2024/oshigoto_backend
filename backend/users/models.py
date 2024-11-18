import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import get_user_model

# User = get_user_model()

class CustomUser(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    # 一意のユーザーID
    email = models.EmailField(unique=True)                                         # メールアドレスを必須・一意に設定
    fa_id = models.CharField(max_length=255, null=True, blank=True)                # Google UID（Firebase用）
    created_at = models.DateTimeField(default=now, editable=False)                 # 作成日時
    updated_at = models.DateTimeField(auto_now=True)                               # 更新日時

    USERNAME_FIELD = 'email'            # 認証に使用するフィールドをメールアドレスに変更
    REQUIRED_FIELDS = ['username']      # スーパーユーザー作成時に必要なフィールド

    def __str__(self):
        return f"{self.username} ({self.email})"        # ユーザーの文字列表現をユーザー名とメールに設定



class UserProfile(models.Model):
    # ユーザータイプの選択肢
    USER_TYPE_CHOICES = [
        ('artist', 'アーティスト'),
        ('creator', '製作者'),
    ]

    GENDER_CHOICES = [
        ('male', '男性'),
        ('female', '女性'),
        ('other', 'その他'),
    ]

    # フィールド定義
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # CustomUserモデルを参照
        on_delete=models.CASCADE,
        related_name='profile'
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)         # ユーザータイプ
    birth_date = models.DateField(null=True, blank=True)                           # 生年月日
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)  # 性別
    created_at = models.DateTimeField(auto_now_add=True)                           # 作成日時
    updated_at = models.DateTimeField(auto_now=True)                               # 更新日時

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"            # ユーザータイプの文字列表現
