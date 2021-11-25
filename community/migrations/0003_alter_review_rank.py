# Generated by Django 3.2.9 on 2021-11-25 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_alter_review_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rank',
            field=models.IntegerField(choices=[(1, '☆'), (2, '★'), (3, '★☆'), (4, '★★'), (5, '★★☆'), (6, '★★★'), (7, '★★★☆'), (8, '★★★★'), (9, '★★★★☆'), (10, '★★★★★')], default=10),
        ),
    ]
