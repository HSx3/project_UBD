from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# def list(request):
#     posts = get_list_or_404(Movie.objects.order_by('-popularity'))

def listing(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3) # Show 5 posts per page

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'posts/index.html', {'posts': posts})
    # post_list = Post.objects.all()
    # paginator = Paginator(page_list, 5) # Show 5 per page
    
    # page = request.GET.get('page')
    # posts = paginator.get_page(page)
    # context = {
    #     'posts': posts,
    # }
    # return render(request, 'posts/index.html', context)



def index(request, movie_pk):
    # posts = get_list_or_404(Post.objects.order_by('-pk'), movie_id=movie_pk)
    posts = Post.objects.filter(movie_id=movie_pk)
    if not posts:
        posts = Post.objects.none()

    context = {
        'movie_pk': movie_pk,
        'posts': posts,
    }
    # return render(request, 'posts/index.html', context)
    
def create(request, movie_pk):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.movie_id = movie_pk
            post.save()
            return redirect('posts:index', movie_pk)
    else:
        post_form = PostForm()
        
    context = {
        'movie_pk': movie_pk,
        'post_form': post_form,
    }
    return render(request, 'posts/create.html', context)
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    movie_pk = post.movie_id
    if request.method == 'POST':
        post.delete()
    return redirect('posts:index', movie_pk)
    
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)
    
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save()
            return redirect('posts:detail', post.pk)
    else:
        post_form = PostForm(instance=post)
    context = {
        'post_form': post_form,
        'post': post,
    }
    return render(request, 'posts/update.html', context)
    
def comment_create(request, post_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_pk
        comment.save()
    return redirect('posts:detail', post_pk)
    # else:
    #     return redirect('posts:detail', post_pk)
    
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.user:
        return redirect('posts:detail', post_pk)
    comment.delete()
    return redirect('posts:detail', post_pk)