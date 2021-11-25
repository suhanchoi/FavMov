# Generated by Django 3.2.9 on 2021-11-25 07:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_moviecomment_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviecomment',
            name='movie_commment_created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moviecomment',
            name='movie_commment_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]