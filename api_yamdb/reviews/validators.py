import datetime

from django.core.exceptions import ValidationError


def validate_score_or_rating(value):
    """Валидатор для оценок и рейтинга."""
    if value not in range(1, 11):
        raise ValidationError(
            'Оценка должна быть в диапазоне от 1 до 10.'
        )


def validate_title_year(value):
    """Валидатор для года."""
    if value > datetime.date.today().year or value < 1:
        raise ValidationError(
            'Нельзя добавить неизданное произведение.'
        )
