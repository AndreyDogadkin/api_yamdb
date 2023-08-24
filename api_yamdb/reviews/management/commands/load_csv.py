import csv
import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, GenreTitle, Comment, Review

User = get_user_model()


class Command(BaseCommand):

    MODELS_FILE_NAMES = {Category: 'category', Genre: 'genre',
                         Title: 'titles', GenreTitle: 'genre_title',
                         User: 'users', Review: 'review', Comment: 'comments'}
    USER_ROLES = {'user': 1, 'moderator': 2, 'admin': 3}

    def handle(self, *args, **options):
        if self.__check_models_objects__():
            for model, file_name in self.MODELS_FILE_NAMES.items():
                self.__add_csv_files_to_db__(model, file_name)
        else:
            sys.exit()

    @classmethod
    def __check_models_objects__(cls):
        exists_objects_models = [m.__name__ for m in cls.MODELS_FILE_NAMES if m.objects.exists()]
        if exists_objects_models:
            answer = input(f'В ваших моделях {", ".join(exists_objects_models)} уже есть данные.\n'
                           'Продолжение операции может привести к конфликтам.\n'
                           'Продолжить? y/n: ')
            if answer.lower() != 'y':
                return False
        return True

    @classmethod
    def __add_csv_files_to_db__(cls, model, file_name: str):
        with open(f'static/data/{file_name}.csv') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                row: dict = row
                if model is Title:
                    category = row.pop('category')
                    model.objects.create(**row, category_id=category)
                elif model is User:
                    role = cls.USER_ROLES.get(row.pop('role'))
                    model.objects.create(**row, role=role)
                elif model in (Review, Comment):
                    author = row.pop('author')
                    model.objects.create(**row, author_id=author)
                else:
                    model.objects.create(**row)
            csvfile.close()
