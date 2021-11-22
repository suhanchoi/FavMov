# Generated by Django 3.2.9 on 2021-11-19 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_moviecomment_rank'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hate_genres',
            field=models.ManyToManyField(related_name='hate_genres', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='user',
            name='like_genres',
            field=models.ManyToManyField(related_name='like_genres', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='user',
            name='like_movies',
            field=models.ManyToManyField(related_name='movies', to='movies.Movie'),
        ),
    ]