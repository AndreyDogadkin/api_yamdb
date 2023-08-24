from rest_framework import serializers
from django.shortcuts import get_object_or_404
from api_yamdb.reviews.models import Title, Genre, Category, GenreTitle, Review, Comment
from rest_framework.exceptions import ParseError


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category',)

    def create(self, validated_data):
        # это нужно будет тестировать, не уверен в этой функции
        genres = validated_data.pop('genre')
        category, _ = Category.objects.get(**validated_data.pop('category'))
        title = Title.objects.create(**validated_data, category=category)

        for genre in genres:
            current_genre, _ = Genre.objects.get(**genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title
            )
        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
    # Не уверен что правильная валидация
    #Эта валидация извлекает значение параметра title_id из запроса,
    #который был передан сериализатору. Контекст запроса содержит 
    #информацию о запросе, включая параметры URL. В данном случае,
    #мы извлекаем значение параметра title_id из контекста запроса и 
    #сохраняем его в переменной title_id для дальнейшего использования.
    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, pk=title_id)
        user = self.context['request'].user
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=user, title=title).exists()
        ):
            raise ParseError(
                'Возможен только один отзыв на произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('review',)
        model = Comment
