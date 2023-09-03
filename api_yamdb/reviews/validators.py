import datetime

from django.core.exceptions import ValidationError


def validate_title_year(value):
    """Валидатор для года."""
    if value > datetime.date.today().year or value < 1:
        raise ValidationError(
            'Нельзя добавить неизданное произведение.'
        )
