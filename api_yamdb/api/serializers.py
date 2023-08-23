from rest_framework import serializers

from api_yamdb.reviews.models import Title, Genre, Category, GenreTitle


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
