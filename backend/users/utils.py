from ..models import Like

def is_matched(user1, user2):
    """
    ユーザー間でマッチが成立しているかを確認する関数。
    """
    return Like.objects.filter(
        sender=user1, receiver=user2, is_matched=True
    ).exists() and Like.objects.filter(
        sender=user2, receiver=user1, is_matched=True
    ).exists()
