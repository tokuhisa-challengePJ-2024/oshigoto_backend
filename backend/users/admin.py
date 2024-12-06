from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,  UserRole, Profile, Like  # UserProfile を削除

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # 管理画面で表示するフィールドを設定
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_id', 'fa_id', 'created_at', 'updated_at')}),  # カスタムフィールドを追加
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_id', 'email', 'fa_id', 'password', 'username')}),  # ユーザー作成時に必要なフィールド
    )

    # 管理画面で表示するリスト項目
    list_display = ('username', 'user_id', 'fa_id', 'email', 'is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'email')
    readonly_fields = ('created_at', 'updated_at')  # 更新や作成日時は読み取り専用


# UserRoleモデルを登録
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at', 'updated_at')  # 表示項目
    list_filter = ('role',)  # フィルタリング可能なフィールド
    search_fields = ('user__email', 'role')  # 検索可能なフィールド


# Profile を管理画面に登録
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_name', 'job_title', 'gender', 'birth_date')  # ユーザー名を追加
    search_fields = ('user__email', 'user__username', 'job_title')  # 検索対象にユーザー名も追加

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'  # 管理画面でのカラム名

    def user_name(self, obj):
        return obj.user.username  # CustomUser の username を表示
    user_name.short_description = 'ユーザー名'  # 管理画面でのカラム名

# いいねモデルを管理画面に登録
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_matched', 'created_at')  # 管理画面で表示するフィールド
    list_filter = ('is_matched', 'created_at')  # フィルタリング
    search_fields = ('sender__email', 'receiver__email')  # 検索対象
    readonly_fields = ('created_at',)  # 作成日時を読み取り専用