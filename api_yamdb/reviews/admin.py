from django.contrib import admin

from . import models


class GenreInline(admin.StackedInline):
    model = models.GenreTitle
    extra = 0


class BaseGenreCategory(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_editable = (
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    empty_value_display = 'Не задано'


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreInline,)
    list_display = (
        'name',
        'year',
        'description',
        'category',
        'get_genre'
    )
    list_editable = (
        'category',
    )
    search_fields = (
        'name',
        'year',
    )
    empty_value_display = 'Не задано'


@admin.register(models.Genre)
class GenreAdmin(BaseGenreCategory):
    pass


@admin.register(models.Category)
class CategoryAdmin(BaseGenreCategory):
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date'
    )
    search_fields = (
        'review',
        'author'
    )


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = (
        'title',
        'score',
        'author'
    )
