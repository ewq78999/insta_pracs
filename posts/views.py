from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-id')

    context = {
        'posts' : posts,
    }

    return render(request, 'index.html', context)



def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post:index')

    else:
        form = PostForm()

    context = {
        'form' : form,
    }

    return render(request, 'form.html', context)


@login_required
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)

        # 현재 로그인 유저
        comment.user = request.user
        # post_id를 기준으로 찾은 post
        post = Post.objects.get(id=post_id)
        comment.post = post

        # comment.post_id = post_id

        comment.save()

        return redirect('posts:index')


@login_required
def like(request, post_id):

    # 좋아요 버튼 누른 유저
    user = request.user
    post = Post.objects.get(id=post_id)

    # 이미 좋아요 버튼 눌렀다면
    if post in user.like_posts.all():
        post.like_users.remove(user)

    # 아직 좋아요 버튼 안 눌렀다면
    else:
        post.like_users.add(user)

    return redirect('posts:index')
