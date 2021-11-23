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


# User의 취향에 맞게 영화 추천해주기
@require_safe
def index(request):

    # genres_id= {12: '모험' , 
    #             '판타지':14, 
    #             '애니메이션': 16, 
    #             '드라마':18 , 
    #             '공포': 27,
    #             '액션':28 ,
    #             '코미디':35,
    #             '역사':36 ,
    #             '서부': 37,
    #             '스릴러': 53,
    #             '범죄':80 ,
    #             '다큐멘터리': 99,
    #             'SF': 878,
    #             '미스터리': 9648,
    #             '음악': 10402,
    #             '로맨스': 10749,
    #             '가족': 10751,
    #             '전쟁': 10752,
    #             'TV 영화': 10770
    #             }


    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    username = request.user.username
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), username=username)

        # QuerySet이 비어있는지 확인을 위한 초기화
        like_genres = 0
        hate_genres = 0
        like_movies = 0

        if person.like_genres.all():
            like_genres = person.like_genres.all()

        if person.hate_genres.all():
            hate_genres = person.hate_genres.all()
        
        if person.like_movies.all():
            like_movies = person.like_movies.all()

        
        print('++++++++++++++++++++++++++**********************************************+++++++++++++++++++*********************************************+++++++++++++++++++*********************************************')

        # !!!!!!!!!!중요!!!!!!!!!
        # Movies/detail 평점 댓글이 있다면, 원래 영화 평점을 대체하고 평점 순으로 정렬
        # !!!!!!!!!!중요!!!!!!!!!


        # 조건문 or 으로 취향이 있는지 없는지 확인 한 후 
        # union 으로 장르 쿼리를 합치고 hate_genres를 제외한 후 
        # 각 장르 수를 잘 따져서 영화 평점 기준 출력 
        # 최종 영화 출력은 몇개로 할건지?

        # 취향 중 좋아하는 장르가 있다면, 해당 Genre QuerySet 생성
        if like_genres != 0:
            like_genres_QS = like_genres

            # 만약 싫어하는 장르가 겹치면 QuerySet에서 삭제
            for i in range(len(hate_genres)):
                like_genres_QS = like_genres_QS.exclude(id=f'{hate_genres[i].id}')

        # 취향에서 선호하는 영화가 있다면, 해당 Movie 에 맞는 Genre QuerySet 생성
        if like_movies != 0:
            like_movies_genres_QS = Genre.objects.none() # 좋아하는 영화들의 장르들
        
            for i in range(len(like_movies)):
                like_movies_genres_QS_filtered = like_movies[i].genres.all()
                for k in range(len(like_movies[i].genres.all())):
                    for j in range(len(hate_genres)):
                        if like_movies[i].genres.all()[k].id == hate_genres[j].id:
                            like_movies_genres_QS_filtered = like_movies_genres_QS_filtered.exclude(id=f'{hate_genres[j].id}')
                like_movies_genres_QS = like_movies_genres_QS.union(like_movies_genres_QS_filtered)
        

        # 취향 중 싫어 하는 장르가 있다면, 위 Genre QuerySet에서 삭제 

        # 둘 다 있다면, 위 QuerySet Union 후, 최종 Movie QuerySet 생성
        if like_genres!= 0 and like_movies != 0 :
            print(1)
            union_like_QS = like_genres_QS.union(like_movies_genres_QS) # 결합
            print(union_like_QS)
            rec_movies = Genre.objects.none()
            for i in range(len(union_like_QS)):
                rec_movies = Movie.objects.filter(genres=f'{union_like_QS[i].id}').union(rec_movies)
                # print('***Movie',(Movie.objects.filter(genres=f'{union_like_QS[i].id}')))
                # print(f'{union_like_QS[i].id}')
                # print('rec_movies',rec_movies)

            # for i in range(len(hate_genres)):
            #         rec_movies = rec_movies.exclude(genres=f'{hate_genres[i].id}')
            
            # 만약 취향 중 싫어하는 장르가 좋아하는 장르와 영화를 모두 삭제시킨 경우, 
            if len(rec_movies) == 0:
                rec_movies = Movie.objects.all()
                for i in range(len(hate_genres)):
                    rec_movies = rec_movies.exclude.filter(genres=f'{hate_genres[i].id}')

        elif like_genres != 0:
            print(2)
            rec_movies = Movie.objects.Movie.objects.none()
            for i in range(len(like_genres_QS)):
                rec_movies = rec_movies.union(Movie.objects.filter(genres=f'{like_genres_QS[i].id}'))
            # for i in range(len(hate_genres)):
            #     rec_movies = rec_movies.exclude(genres=f'{hate_genres[i].id}')

        elif like_movies != 0:
            print(3)
            rec_movies = Movie.objects.none()
            for i in range(len(like_movies_genres_QS)):
                rec_movies = rec_movies.union(Movie.objects.filter(genres=f'{like_movies_genres_QS[i].id}'))
            # for i in range(len(hate_genres)):
            #     rec_movies = rec_movies.exclude(genres=f'{hate_genres[i].id}')

        # 만약 취향 중 싫어하는 장르만 있다면, Movie 평점 순으로 불러온 후, 삭제
        else :
            print(4)
            rec_movies = Movie.objects.all()
            print(rec_movies)
            for i in range(1):
                rec_movies = rec_movies.exclude(genres=f'{hate_genres[i].id}')

        # print(rec_movies)
        # rec_movies = rec_movies.order_by('vote_average').distinct()
        rec_movies = rec_movies[:6] # 갯수 할당 # 이때 삭제??
    
        print('rec_movies',rec_movies)
        print('hate_genres',hate_genres)
        # 추천 영화들 장르와 취향 추천 장르들 출력 후 비교
        for i in range(len(rec_movies)):
            print('recommend_movie', rec_movies[i].genres.all())
            # pass

        if like_genres!= 0 and like_movies != 0:
            print('union_like_QS',union_like_QS)
        
        elif like_genres != 0:
            print('like_genres_QS',like_genres_QS)
        
        elif like_movies != 0:
            print('like_movies_genres_QS',like_movies_genres_QS)



    # 3

    # /movies/?page=2 ajax 요청 => json
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = serializers.serialize('json', page_obj)
        return HttpResponse(data, content_type='application/json')
    # /movies/ 첫번째 페이지 요청 => html
    else:
        context = {
            'movies': page_obj,
            'rec_movies':rec_movies,
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


