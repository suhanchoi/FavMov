# Generated by Django 3.2.9 on 2021-11-05 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='movies.Genre'),
        ),
    ]
