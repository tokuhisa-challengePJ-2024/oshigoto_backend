from rest_framework import serializers
from django.contrib.auth import get_user_model

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