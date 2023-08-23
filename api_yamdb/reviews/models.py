from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_title_year, validate_score_or_rating


User = get_user_model()


class Review(models.Model):
    """Отзывы пользователей и их контент."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рецензируемое произведение'
    )
    text = models.TextField(
        max_length=5000,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.SmallIntegerField(
        verbose_name='Оценка произведения пользователем'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания отзыва'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Отзыв. model Review'
        verbose_name_plural = 'Отзывы. model Review'


class Comment(models.Model):
    """Комментарии пользователей на отзывы."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв'
    )
    text = models.TextField(
        max_length=2000,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания комментария'
    )

    class Meta:
        ordering = ('review', 'author')
        verbose_name = 'Комментарий. model Comment'
        verbose_name_plural = 'Комментарии. model Comment'


class BaseCategoryGenreModel(models.Model):
    """Базовая модель для жанров и категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True


class Category(BaseCategoryGenreModel):
    """ Модель категорий. """

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Genre(BaseCategoryGenreModel):
    """Модель жанров."""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=(validate_title_year,),
        verbose_name='Год выпуска'
    )
    rating = models.SmallIntegerField(
        default=models.SET_NULL,
        null=True,
        validators=(validate_score_or_rating,),
        verbose_name='Рейтинг'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'произведения'


class GenreTitle(models.Model):
    """Вспомогательная модель жанров и произведений"""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('title', 'genre'),
            name='genre_title_uniq'),
        )

