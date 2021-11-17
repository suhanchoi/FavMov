from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.http import require_safe
from .models import Movie, Genre, MovieComment
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
from .forms import MovieCommentForm


# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # /movies/?page=2 ajax 요청 => json
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = serializers.serialize('json', page_obj)
        return HttpResponse(data, content_type='application/json')
    # /movies/ 첫번째 페이지 요청 => html
    else:
        context = {
            'movies': page_obj,
        }

        return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_comments = movie.moviecomment_set.all()
    movie_comment_form = MovieCommentForm()
    context = {
        'movie': movie,
        'movie_comment_form': movie_comment_form,
        'movie_comments': movie_comments,
    }
    return render(request, 'movies/detail.html', context)

@require_POST
def create_movie_comment(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_comment_form = MovieCommentForm(request.POST)
    if movie_comment_form.is_valid():
        movie_comment = movie_comment_form.save(commit=False)
        movie_comment.movie = movie
        movie_comment.user = request.user
        movie_comment.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'movie_comment_form': movie_comment_form,
        'movie': movie,
        'movie_comments': movie.moviecomment_set.all(),
    }
    return render(request, 'movies/detail.html', context)


@require_POST
def delete_movie_comment(request, movie_pk, moviecomment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_comment = get_object_or_404(MovieComment, pk=moviecomment_pk)
    if request.user == movie_comment.user:
        movie_comment.delete()
    return redirect('movies:detail', movie.pk)




@require_safe
def recommended(request):
    if request.user.is_authenticated:
        pass