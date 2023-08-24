from reviews.models import Title, GenreTitle, Category
from .serializers import TitleSerializer
from rest_framework import viewsets


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    serializer_class = TitleSerializer

