from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Title, Genre, Category, Review, Comment


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
        response['genre'] = [GenreSerializer(g).data
                             for g in instance.genre.all()]
        return response


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('title',)
        model = Review

    def create(self, validated_data):
        title = validated_data.get('title')
        user = validated_data.get('author')
        if Review.objects.filter(title=title, author=user).exists():
            raise ValidationError('Возможен только один '
                                  'отзыв на произведение.')
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('review',)
        model = Comment
