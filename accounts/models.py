from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre, Movie

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    like_genres = models.ManyToManyField(Genre, null =True, blank = True, related_name="like_genres")
    hate_genres = models.ManyToManyField(Genre, null =True, blank = True, related_name="hate_genres")
    like_movies = models.ManyToManyField(Movie, null =True, blank = True, related_name="like_movies")

# 유저의 취향 좋아하는 장르 , 싫어하는 장르, 선호하는 영화
# 장르는 char로 받은 다음에 integer로 매칭 -> 
# movies.genre id <-> name 으로 매칭
# movies_movie_genres 으로 m:n movie_id, genre_id 로 매칭