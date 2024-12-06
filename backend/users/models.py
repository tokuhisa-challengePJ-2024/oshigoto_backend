import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.conf import settings


class CustomUser(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    # 一意のユーザーID
    email = models.EmailField(unique=True)                                         # メールアドレスを必須・一意に設定
    fa_id = models.CharField(max_length=255, null=True, blank=True)                # Google UID（Firebase用）
    created_at = models.DateTimeField(default=now, editable=False)                 # 作成日時
    updated_at = models.DateTimeField(auto_now=True)                               # 更新日時
    # is_artist = models.BooleanField(default=False)                                 # アーティストフラグ user role作成のため削除
    USERNAME_FIELD = 'email'            # 認証に使用するフィールドをメールアドレスに変更
    REQUIRED_FIELDS = ['username']      # スーパーユーザー作成時に必要なフィールド

    def __str__(self):
        return f"{self.username} ({self.email})"        # ユーザーの文字列表現をユーザー名とメールに設定


class UserRole(models.Model):
    ROLE_CHOICES = [
        ('artist', 'アーティスト'),
        ('creator', '製作者'),
        ('admin', '管理者'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ユーザーと紐付ける
        on_delete=models.CASCADE,
        related_name='roles'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # 役割
    created_at = models.DateTimeField(auto_now_add=True)          # 作成日時
    updated_at = models.DateTimeField(auto_now=True)              # 更新日時

    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"


class Profile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # 一意のプロフィールID
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ユーザーと紐付け
        on_delete=models.CASCADE,
        related_name="profile"
    )
    user_name = models.CharField(max_length=255, verbose_name="ユーザー名", null=True, blank=True)  # ユーザー名

    profile_image = models.ImageField(
        upload_to='profile_images/',  # 保存先のディレクトリ
        null=True,
        blank=True,
        verbose_name="プロフィール画像"
    )

    GENDER_CHOICES = [
        ('男性', '男性'),
        ('女性', '女性'),
        ('選択しない', '選択しない'),
    ]

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default='選択しない'
    )  # 性別
    
    birth_date = models.DateField(null=True, blank=True)  # 生年月日
    
    agency_or_group = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="所属（事務所やグループ名）"
    ) 

    job_title = models.CharField(max_length=255, verbose_name="職業")
    workhistory = models.TextField(null=True, blank=True, verbose_name="経歴")
    awards = models.TextField(null=True, blank=True, verbose_name="受賞歴")
    skills = models.TextField(null=True, blank=True, verbose_name="スキル")
    portfolio = models.TextField(null=True, blank=True, verbose_name="ポートフォリオ")
    specialization = models.TextField(null=True, blank=True, verbose_name="得意分野")
    challenges = models.TextField(null=True, blank=True, verbose_name="挑戦したいこと")
    dislikes = models.TextField(null=True, blank=True, verbose_name="NGなこと")
    free_text = models.TextField(null=True, blank=True, verbose_name="フリー記述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return f"{self.user.email} - {self.job_title}"


class Like(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_sent"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_received"
    )
    is_matched = models.BooleanField(default=False)  # マッチング成立フラグ
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'receiver'], name='unique_like')
        ]

    def __str__(self):
        return f"{self.sender.email} -> {self.receiver.email} ({'Matched' if self.is_matched else 'Pending'})"
    

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_sent'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_received'
    )
    content = models.TextField(verbose_name="メッセージ内容")
    created_at = models.DateTimeField(default=now, verbose_name="送信日時")
    is_read = models.BooleanField(default=False, verbose_name="既読フラグ")

    class Meta:
        ordering = ['-created_at']  # 最新のメッセージが最初に来るように
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender=models.F('receiver')),
                name='prevent_self_message'  # 自分自身へのメッセージを禁止
            )
        ]

    def __str__(self):
        return f"{self.sender.email} -> {self.receiver.email}: {self.content[:20]}..."