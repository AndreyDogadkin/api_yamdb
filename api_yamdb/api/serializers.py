from rest_framework import serializers

from reviews.models import Title, Genre, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(required=True,
                                         queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True)
    category = serializers.SlugRelatedField(required=True,
                                            queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        response['genre'] = [GenreSerializer(i).data for i in instance.genre.all()]
        return response
