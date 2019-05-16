from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q
from .models import Movie, Score, Genre
from accounts.models import User
from .forms import MovieForm, ScoreForm
from django.core.paginator import Paginator

# Create your views here.
# 홈
@login_required
def index(request):
    user = request.user
    movie = Movie.objects.all()
    movie = movie.exclude(saw_user=user)
    popular_movies = movie.order_by('-popularity')[0:60]
    highest_movies = movie.order_by('-vote_average')[0:min(60, movie.count())]
    user_movie =  user.like_movie.all().order_by('?')[0:min(60, movie.count())]
    play_movie_1 = movie.order_by('-popularity')[0]
    random_movie = movie.order_by('?')[0]
    followings = User.objects.filter(followers=user)
    if followings:
        following = followings.order_by('?')[0]
        following_saw = Movie.objects.filter(saw_user=following)
        following_saw = following_saw.exclude(Q(saw_user=user) | Q(vote_average__lt=7))
        following_saw = following_saw.order_by('-vote_average')[0:min(60, Movie.objects.all().count())]
    else:
        following_saw = Movie.objects.none()
    genres_count = []
    genres = Genre.objects.all()
    max_count = 0
    for genre in genres:
        count = genre.genre_movie.count()
        if count >= max_count:
            max_count = count
            max_genre = genre
    favorite_genre = max_genre.genre_movie.all()
    favorite_genre = favorite_genre.exclude(saw_user=user)[:min(60, favorite_genre.all().count())]
    # user_saw = Movie.objects.filter(saw_user=user)
    # genres = Genre.objects.filter(genre_movie=user_saw)
    context = {
        'popular_movies': popular_movies,
        'highest_movies': highest_movies,
        'user': user,
        'user_movie': user_movie,
        'random_movie': random_movie,
        'following_saw': following_saw,
        'favorite_genre': favorite_genre,
    }
    return render(request, 'movies/index.html', context)



# 영화 리스트    
@login_required
def list(request):
    # movies = get_list_or_404(Movie.objects.order_by('-popularity'))[0:10]
    popular_movies = Movie.objects.all().order_by('-popularity')[0:60]
    highest_movies = Movie.objects.all().order_by('-vote_average')[0:60]
    context = {
        'popular_movies': popular_movies,
        'highest_movies': highest_movies,
    }
    return render(request, 'movies/list.html', context)
    
def main(request):
    movies = get_list_or_404(Movie.objects.order_by('-popularity'))[0:10]
    context = {
        'movies': movies,
    }
    return render(request, 'movies/test.html', context)
    
# 영화 생성
# @login_required
# def create(request):
#     # if request.user.is_superuser:
            
#     if request.method == 'POST':
#         movie_form = MovieForm(request.POST)
#         if movie_form.is_valid():
#             movie = movie_form.save(commit=False)
#             movie.user = request.user
#             movie.save()
#             return redirect('movies:list')
#     else:
#         movie_form = MovieForm()
#     context = {
#         'movie_form': movie_form,
#     }
#     return render(request, 'movies/create.html', context)
    
    # else:
    #     return render()

# 영화정보 수정    
# @login_required
# def update(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
    
#     # if movie.user != request.user:
#     #     return redirect('movies:list')
    
#     if request.method == 'POST':
#         movie_form = MovieForm(request.POST, instance=movie)
#         if movie_form.is_valid():
#             movie = movie_form.save()
#             return redirect('movies:list')
            
#     else:
#         movie_form = MovieForm(instance=movie)
#     context = {
#         'movie_form': movie_form,
#         'movie': movie,
#     }
#     return render(request, 'movies/update.html', context)

# 영화 상세
@login_required
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    actors = movie.cast_set.all()[0:5]
    score_form = ScoreForm()
    context = {
        'movie': movie,
        'score_form': score_form,
        'actors': actors,
    }
    return render(request, 'movies/detail.html', context)

# 영화 삭제
# def delete(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
    
#     # if movie.user != request.user:
#     #     return redirect('movies:list')
        
#     if request.method == 'POST':
#         movie.delete()
#     return redirect('movies:list')
    
# 평 생성
@login_required
@require_POST
def score_create(request, movie_pk):
    form = ScoreForm(request.POST)
    if form.is_valid():
        score = form.save(commit=False)
        score.user = request.user
        score.movie_id = movie_pk
        score.save()
        movie = get_object_or_404(Movie, pk=movie_pk)
        movie.saw_user.add(request.user)
        total = movie.vote_count * movie.vote_average
        total += score.score
        movie.vote_count += 1
        movie.vote_average = round(total / movie.vote_count, 2)
    # 점수 변경 추가하기
        return redirect('movies:detail', movie_pk)
    else:
        return redirect('movies:list')

# 평 삭제
@login_required
def score_delete(request, movie_pk, score_pk):
    score = get_object_or_404(Score, pk=score_pk)
    num = score.score
    score.delete()
    movie = get_object_or_404(Movie, pk=movie_pk)
    total = movie.vote_average * movie.vote_count
    total -= num
    movie.vote_count -= 1
    movie.vote_average = round(total / movie.vote_count, 2)
    movie.saw_user.remove(request.user)
    # 점수 변경 추가하기
    return redirect('movies:detail', movie_pk)

@login_required
def score_update(request, movie_pk, score_pk):
    score = get_object_or_404(Score, pk=score_pk)
    old = score.score
    
    # if movie.user != request.user:
    #     return redirect('movies:detail')
    
    if request.method == 'POST':
        score_form = ScoreForm(request.POST, instance=score)
        if score_form.is_valid():
            scores = score_form.save()
            new = scores.score
            movie = get_object_or_404(Movie, pk=movie_pk)
            total = movie.vote_count * movie.vote_average
            total += (new - old)
            movie.vote_average = round(total / movie.vote_count, 2)
            return redirect('movies:detail', movie_pk)
            
    else:
        score_form = ScoreForm(instance=score)
    context = {
        'score_form': score_form,
        # 'score': score,
        # 'movie_pk': movie_pk,
    }
    return render(request, 'movies/score_update.html', context)


    
# 영화 보고싶어요
@login_required
def like(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
            liked = False
            movie.popularity -= 1
        else:
            movie.like_users.add(request.user)
            liked = True
            movie.popularity += 1
        return JsonResponse({'liked': liked})
    else:
        return HttpResponseBadRequest()

# 영화 관심없어요
# @login_required
# def hate(request, movie_pk):
#     if request.is_ajax():
#         movie = get_object_or_404(Movie, pk=movie_pk)
#         if request.user in movie.hate_users.all():
#             movie.hate_users.remove(request.user)
#             hated = False
#             liked = False
#         else:
#             movie.hate_users.add(request.user)
#             if request.user in movie.like_users.all():
#                 liked = True
#             hated = True
#         context = {
#             'liked': liked,
#             'hated': hated
#         }
#         return JsonResponse(context)
#     else:
#         return HttpResponseBadRequest()
    
    
# 보고싶어요 / 관심없어요
@login_required
def wishes(request):
    user = request.user
    movie = Movie.objects.all()
    movie = movie.exclude(saw_user=user)
    movies = movie.order_by('-popularity')
    if not movies:
        movies = Movie.objects.none()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/wishes.html', context)
    
# 평가하기
@login_required
def evaluate(request):
    movies = get_list_or_404(Movie.objects.all().order_by('-popularity'))
    paginator = Paginator(movies, 6)
    page = request.GET.get('page')
    movie_list = paginator.get_page(page)
    context = {
        'movies': movies,
        'movie_list': movie_list,
    }
    return render(request, 'movies/evaluate.html', context)
    
    
@login_required
def search(request):
    if request.is_ajax():
        title = request.POST.get('title', None)
        title = ''
        statuss = Movie.objects.filter(title__contains=title)
        context = {
            'statuss': statuss
        }
        print(statuss)
        return render(request, 'movies/index.html', context)
    else:
        return HttpResponseBadRequest()

@login_required
def search_result(request):
    print('hi')
    return
        
# 추천 페이지
@login_required
def popularity(request):
    movie = Movie.objects.all()
    popular_movies = movie.order_by('-popularity')[0:60]
    context = {
        'popular_movies': popular_movies,
    }
    return render(request, 'movies/popularity_list.html', context)
    
def highest(request):
    movie = Movie.objects.all()
    highest_movies = movie.order_by('-vote_average')[0:60]
    context = {
        'highest_movies': highest_movies,
    }
    return render(request, 'movies/highest_list.html', context)
    # user_movie =  user.like_movie.all().order_by('?')[0:min(60, movie.count())]