# Generated by Django 3.2 on 2023-08-27 17:57

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_genretitle_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['id'], 'verbose_name': 'Жанр', 'verbose_name_plural': 'жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['id'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'произведения'},
        ),
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.PositiveSmallIntegerField(null=True, validators=[reviews.validators.validate_score_or_rating], verbose_name='Рейтинг'),
        ),
    ]
