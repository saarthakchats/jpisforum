from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:

        if request.user.is_staff:
            posts = Post.objects.all().order_by('-votes_total')
            return render(request, 'posts/home.html', {'posts': posts})
        else:
            posts = Post.objects.all().order_by('-votes_total').filter(post_approved=True)
            if len(posts) == 0:
                error = True
            else:
                error = False
            return render(request, 'posts/home.html', {'posts': posts, 'error': error})
    else:
        return render(request, 'posts/landing.html')

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

@login_required(login_url='/accounts/signup')
def detail(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        all_upvoted_users = post.upvoted_users.split(',')
        print(all_upvoted_users,request.user.username)
        if str(request.user.username) in all_upvoted_users:
            return render(request, 'posts/detail.html', {'post': post,'error':'You have already upvoted'})

        else:
            post.votes_total += 1
            current_user = request.user
            post.upvoted_users = post.upvoted_users + current_user.username + ','
            post.save()
            return render(request, 'posts/detail.html', {'post': post})

    else:
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'posts/detail.html', {'post': post})

def approve(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        approved_by_users = post.approved_by.split(',')
        if request.user.username in approved_by_users:
            return render(request, 'posts/detail.html', {'post': post,'error':'You have already approved'})
        else:
            post.approved_by = post.approved_by + request.user.username + ','
            post.post_approvals += 1
            if post.post_approvals == 3:
                post.post_approved = True
            post.save()
            return render(request, 'posts/detail.html', {'post': post})
    else:
        return render(request, 'posts/home.html')
