from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_title_year, validate_score_or_rating

User = get_user_model()


class Review(models.Model):
    """Отзывы пользователей и их контент."""

    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE,
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
        verbose_name='Оценка произведения пользователем',
        validators=[validate_score_or_rating, ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания отзыва'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = (models.UniqueConstraint(
            fields=('title', 'author'),
            name='author_title_uniq'),
        )

    def __str__(self):
        return (
            f'Отзыв к произведению {self.title} от {self.author}'
        )


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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


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
    """Модель категорий."""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'
        ordering = ['id']


class Genre(BaseCategoryGenreModel):
    """Модель жанров."""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'
        ordering = ['id']


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
    rating = models.PositiveSmallIntegerField(
        null=True,
        validators=[validate_score_or_rating, ],
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

    def get_genre(self):
        return ", ".join([str(p) for p in self.genre.all()])

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'произведения'
        ordering = ['id']


class GenreTitle(models.Model):
    """Вспомогательная модель жанров и произведений"""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.genre.name

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('title', 'genre'),
            name='genre_title_uniq'),
        )
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
