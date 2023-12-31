from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.conf import settings
import os
import fun
import subprocess


def home(request):
    return render(request,'home.html')


def signup(request):
    if not request.user.is_anonymous:
        return redirect("/udash")
    
    if request.method=="POST":

        User = get_user_model()
        users = User.objects.all()
        user_list=[]
        email_list=[]
        for i in users:
            user_list.append(i.username)
            email_list.append(i.email)

        acc_type=str(request.POST.get('IN_OC'))

        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        if email in email_list:
            messages.error(request, 'Email already signed up. Head to login page.')
            return render(request,'signup.html')
        if name in user_list:
            messages.error(request, 'Username already exists. Get another username')
            return render(request,'signup.html')
        
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()

        npath = os.path.join('../ScreenshotRecorder/static/screenrecordings', name)

        os.mkdir(npath)

        messages.success(request, f'Your account was created. Your username is {name}. Head to login page')
        
    return render(request,'signup.html')


def loginuser(request):
    if not request.user.is_anonymous:
        return redirect('/udash')
    if request.method=="POST":
        username=request.POST.get('ID')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('/udash')
        else:
            messages.error(request, 'Wrong username or password')
            return render(request,'login.html')
    return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/loginuser')

def udash(request):
    if request.user.is_anonymous:
        return redirect('/loginuser')
    
    name=request.user.username
    video_list=fun.video_list(name)

    dic={'video_list':video_list,'name':name}
    return render(request,'udash.html',dic)

def recscreen(request):
    if request.user.is_anonymous:
        return redirect('/loginuser')
    fun.newrecording(request.user.username)
    os.popen('py popupapp.py')
    return redirect('/udash')


def vid(request):
    if request.user.is_anonymous:
        return redirect("/loginuser")
    
    video = request.GET.get('video')  # Retrieve the ps_id from the URL query parameters
    name = request.user.username
    path = f"static/screenrecordings/{name}/{video}"

    subprocess.Popen(['start', '', path], shell=True)

    return redirect("/udash")

    # return render(request, 'vid.html', {"path":path})