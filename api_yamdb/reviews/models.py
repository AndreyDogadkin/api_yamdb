from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    """Отзывы пользователей и их контент."""

    SCORE_CHOICES = (
        (1, '1. Очень плохо. Не понравилось совсем.'),
        (2, '2. Плохо. Не понравилось почти всё.'),
        (3, '3. Не очень. Не понравилось многое.'),
        (4, '4. Так себе. Мало что понравилось.'),
        (5, '5. Ни то, ни сё. Почти ничего не понравилось.'),
        (6, '6. Неплохо. Кое-что понравилось.'),
        (7, '7. Хорошо. Многое понравилось.'),
        (8, '8. Очень хорошо. Почти всё понравилось.'),
        (9, '9. Великолепно. Очень понравилось.'),
        (10, '10. Высший балл. В восторге.'),
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        max_length=6000,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.SmallIntegerField(
        choices=SCORE_CHOICES,
        verbose_name='Оценка произведения пользователем'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания отзыва'
    )

    class Meta:
        pass


class Comment(models.Model):
    """Комментарии пользователей на отзывы."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв'
    )
    text = models.TextField(
        max_length=1500,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания комментария'
    )

    class Meta:
        pass
