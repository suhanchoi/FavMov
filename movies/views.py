from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.http import require_safe
from .models import Movie, Genre, MovieComment
from accounts.models import User
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
from .forms import MovieCommentForm


# 여기다가 user의 취향에 맞게 영화 추천해주기
@require_safe
def index(request):

    
    genres_id= {12: '모험' , 
                '판타지':14, 
                '애니메이션': 16, 
                '드라마':18 , 
                '공포': 27,
                '액션':28 ,
                '코미디':35,
                '역사':36 ,
                '서부': 37,
                '스릴러': 53,
                '범죄':80 ,
                '다큐멘터리': 99,
                'SF': 878,
                '미스터리': 9648,
                '음악': 10402,
                '로맨스': 10749,
                '가족': 10751,
                '전쟁': 10752,
                'TV 영화': 10770
                }


    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    username = request.user.username
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), username=username)

        like_genres = person.like_genres.all()
        hate_genres = person.hate_genres.all()
        like_movies = person.like_movies.all()
        
        print('++++++++++++++++++++++++++**********************************************+++++++++++++++++++*********************************************+++++++++++++++++++*********************************************')
        print(like_genres)
        print(like_genres[0].id)
        
        # 조건문 or 으로 취향이 있는지 없는지 확인 한 후 
        # union 으로 장르 쿼리를 합치고 hate_genres를 제외한 후 
        # 각 장르 수를 잘 따져서 영화 평점 기준 출력 
        # 최종 영화 출력은 몇개로 할건지?

        
        rec_movies_genre = Movie.objects.filter(genres=f'{like_genres[0].id}')
        rec_movies_genre = rec_movies_genre[:3] # 3개만 할당
        
        print(like_movies)
        print(like_movies[0])
        print("저거",like_movies[0].genres.all())
        # rec_movies_movie = Movie.objects.filter(genres=f'{like_movies[0].id}')
        
        print("이거",rec_movies_genre)
        print(like_genres)
        rec_movie = like_genres.union(like_movies[0].genres.all())
        print("최종",rec_movie)

    # 3

    # /movies/?page=2 ajax 요청 => json
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = serializers.serialize('json', page_obj)
        return HttpResponse(data, content_type='application/json')
    # /movies/ 첫번째 페이지 요청 => html
    else:
        context = {
            'movies': page_obj,
            'rec_movies_genre':rec_movies_genre,
        }

        return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):

    STARS = [
        '',
        '☆',
        '★',
        '★☆',
        '★★',
        '★★☆',
        '★★★',
        '★★★☆',
        '★★★★',
        '★★★★☆',
        '★★★★★'
    ]

    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_comments = movie.moviecomment_set.all()
    movie_comment_form = MovieCommentForm()
    rank_sum = 0
    rank_cnt = 0
    rank_avg = 0
    for comment in movie_comments:
        comment.star = STARS[comment.rank]
        rank_sum += int(comment.rank)
        rank_cnt += 1
    if rank_cnt >= 1:
        rank_avg = round(rank_sum / rank_cnt,2)
    
    context = {
        'movie': movie,
        'movie_comment_form': movie_comment_form,
        'movie_comments': movie_comments,
        'rank_avg' : rank_avg,
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
        # movie_rank = movie.moviecomment_set.rank
        return redirect('movies:detail', movie.pk)
    context = {
        'movie_comment_form': movie_comment_form,
        'movie': movie,
        'movie_comments': movie.moviecomment_set.all(),
        'movie_rank': movie.moviecomment_set.rank,
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


