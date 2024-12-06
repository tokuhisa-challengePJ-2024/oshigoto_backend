from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']          # 必要なフィールドだけ指定
        extra_kwargs = {
            'password': {'write_only': True},   # パスワードは書き込み専用
        }

    def create(self, validated_data):
        # usernameを自動生成（emailの先頭部分を使用）
        email = validated_data['email']
        username = email.split('@')[0]

        # create_user メソッドでユーザー作成
        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password']
        )
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)  # プロフィール画像の追加
    user_id = serializers.UUIDField(source='user.user_id', read_only=True)  # UUID形式のuser_idを含める

    class Meta:
        model = Profile
        fields = [
            'user', 'user_id', 'user_name', 'profile_image', 'gender', 'birth_date',
            'agency_or_group', 'job_title', 'workhistory', 'awards', 'skills',
            'portfolio', 'specialization', 'challenges', 'dislikes', 'free_text'
        ]
        extra_kwargs = {
            'user': {'read_only': True},       # userフィールドを読み取り専用
            'user_name': {'required': True},   # user_nameを必須フィールドに設定
        }

    def create(self, validated_data):
        # 新しいプロフィールを作成
        profile = Profile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        # プロフィールを更新
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProfileDataSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()  # プロフィール画像のURLを含める

    class Meta:
        model = Profile
        fields = [
            'user_name', 'profile_image_url', 'gender', 'birth_date',
            'agency_or_group', 'job_title', 'workhistory', 'awards',
            'skills', 'portfolio', 'specialization', 'challenges',
            'dislikes', 'free_text'
        ]

    def get_profile_image_url(self, obj):
        # プロフィール画像のURLを取得
        if obj.profile_image:
            return obj.profile_image.url
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user_id', read_only=True)   # CustomUserのUUIDフィールドを指定
    profile = ProfileDataSerializer(read_only=True)                     # プロフィール情報をネスト
    roles = serializers.SerializerMethodField()                         # ユーザーのロール情報を追加

    class Meta:
        model = User
        fields = ['user_id', 'email', 'roles', 'profile']  # UUIDのuser_id、email、roles、profile

    def get_roles(self, obj):
        # UserRoleモデルから現在のユーザーに関連するロールを取得
        return list(obj.roles.values('role'))  # roleのみ取得