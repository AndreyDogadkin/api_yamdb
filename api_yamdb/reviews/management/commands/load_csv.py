import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, GenreTitle, Comment, Review

User = get_user_model()


class Command(BaseCommand):

    MODELS_FILE_NAMES = {Category: 'category', Genre: 'genre',
                         Title: 'titles', GenreTitle: 'genre_title',
                         User: 'users', Review: 'review', Comment: 'comments'}

    def handle(self, *args, **options):
        for model, file_name in self.MODELS_FILE_NAMES.items():
            self.__add_csv_files_to_db__(model, file_name)

    @staticmethod
    def __add_csv_files_to_db__(model, file_name: str):
        with open(f'static/data/{file_name}.csv') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                row: dict = row
                if model is Title:
                    category = Category.objects.get(id=row.pop('category'))
                    model.objects.create(**row, category=category)
                else:
                    model.objects.create(**row)
            csvfile.close()
