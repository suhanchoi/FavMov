# Generated by Django 3.2.9 on 2021-11-19 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_moviecomment_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviecomment',
            name='rank',
            field=models.IntegerField(choices=[(1, '☆'), (2, '★'), (3, '★☆'), (4, '★★'), (5, '★★☆'), (6, '★★★'), (7, '★★★☆'), (8, '★★★★'), (9, '★★★★☆'), (10, '★★★★★')], default=10),
        ),
    ]
