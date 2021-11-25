from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/comments/create/', views.create_movie_comment, name='create_movie_comment'),
    path('<int:movie_pk>/comments/<int:moviecomment_pk>/delete/', views.delete_movie_comment, name='delete_movie_comment'),
    path('<int:movie_pk>/like/', views.like, name='like'),
]
