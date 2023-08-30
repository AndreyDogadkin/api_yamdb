from django_filters import FilterSet, CharFilter
from reviews.models import Title


class TitleFilterSet(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
