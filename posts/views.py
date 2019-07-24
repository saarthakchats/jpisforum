from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from django.contrib.auth.models import User
def home(request):
    posts = Post.objects
    return render(request, 'posts/home.html', {'posts': posts})

@login_required(login_url='/accounts/signup')
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body']:
            post = Post()
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.pubdate = timezone.datetime.now()
            post.hunter = request.user
            ano = request.POST['poi']
            if  ano == 'y':
                post.anonymous = True
            else:
                post.anonymous = False
            post.save()
            # return redirect('/posts/' + str(post.id))
            return render(request, 'posts/create.html')
        else:
            return render(request, 'posts/create.html', {'error': 'Sorry, missing fields'})
    else:
        return render(request, 'posts/create.html')

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/detail.html', {'post': post})
