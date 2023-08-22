from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    """Отзывы пользователей и их контент."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        max_length=6000
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField(
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        pass


class Comment(models.Model):
    """Комментарии пользователей на отзывы."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        max_length=1500
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        pass
