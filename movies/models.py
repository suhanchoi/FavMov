from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=50)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name="movies")
    #like users 추가 

class MovieComment(models.Model):
    content = models.TextField()
    RANKS = [
        (1, '☆'),
        (2, '★'),
        (3, '★☆'),
        (4, '★★'),
        (5, '★★☆'),
        (6, '★★★'),
        (7, '★★★☆'),
        (8, '★★★★'),
        (9, '★★★★☆'),
        (10,'★★★★★'),
    ]
    rank = models.IntegerField(choices=RANKS, default=10)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
