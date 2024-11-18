from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

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

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'birth_date', 'gender', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user_type', 'gender')