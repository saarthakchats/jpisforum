from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Register
from posts.models import Post
import datetime
import smtplib
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirmpass']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username has been taken'})
            except User.DoesNotExist:
                mail = request.POST['email']
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'], email=mail)
                global sign_up_code
                sign_up_code = genOTP(mail)
                register = Register(user=user, OTP=sign_up_code)
                register.save()
                print(sign_up_code)
                return render(request,'accounts/verifyOTP.html')
        else:
            return render(request, 'accounts/signup.html', {'error': "Passwords don't match"})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.register.IsVerified:
                auth.login(request, user)
                return redirect('home')
            else:
                return render(request, 'accounts/login.html', {'error': "Your account was not verified and is deleted for security reasons"})
        else:
            return render(request, 'accounts/login.html', {'error': "User not found"})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

def genOTP(mail):
    multiplier1 = str(datetime.datetime.now()).split('.')[1]
    multiplier2 = str(len(mail) % 100)
    OTP = int(multiplier1+multiplier2)
    subject = 'Your OTP'
    message = str(OTP)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mail,]
    send_mail( subject, message, email_from, recipient_list )
    return OTP

def verifyOTP(request):
    global sign_up_code
    print(int(request.POST['OTP']),sign_up_code)
    if int(request.POST['OTP']) == sign_up_code:
        current_register = Register.objects.get(OTP=sign_up_code)
        user = User.objects.get(register=current_register)
        current_register.IsVerified = True
        current_register.save()
        auth.login(request, user)
        return redirect('home')
    else:
        error = 'Incorrect OTP'
        return render(request,'accounts/verifyOTP.html', {'error':error})

def userpage(request, user_name):
    man = get_object_or_404(User, username=user_name)
    posts = Post.objects.all().filter(hunter=man)
    considered_posts = Post.objects.all().filter(hunter=man,post_considered=True)
    other_posts = Post.objects.all().filter(hunter=man,post_considered=False)
    num_posts = len(posts)
    num_considered_posts = len(considered_posts)
    num_other_posts = len(other_posts)

    return render(request, 'accounts/userpage.html', {'man': man,'posts':posts,'num_posts':num_posts,'num_considered_posts':num_considered_posts,'num_other_posts':num_other_posts})
