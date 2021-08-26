from django.shortcuts import render , redirect

from django.contrib.auth.decorators import login_required 
from accounts.models import Course , Profile

from .forms import StreamForm , CourseForm
from .models import Stream , Video

import urllib.request
import os
from urllib.error import HTTPError

from urllib.parse import unquote , quote

import secrets

from django.contrib import messages

def checkStream(url):
    url = 'http://192.168.1.7:8080/hls/test.m3u8'
    try:
        code = urllib.request.urlopen(url).getcode()
        if str(code).startswith('2') or str(code).startswith('3') :
            print('Stream is working')
            return True
        else:
            print('Stream is dead')
            return False
    except HTTPError :
        print("Stream is dead") 
        return False
       

def indexPage(request):
    return render(request,'root/index.html')
  
def contactPage(request):
    return render(request,'root/contact.html')
     

@login_required(login_url="login")
def streamsPage(request):
    #student = Profile.objects.filter(user=request.user)
    #courses = Course.objects.filter(students=student[0])
    if request.method == "POST":
        code = request.POST.get('code','')
        if code is not None:
            if(len(code) != 11):
                messages.error(request,'Please enter a valid stream code.')
                return redirect('/streams')

            return redirect('/streams/'+ code + '/')
     
    all_courses = Course.objects.all()
    context = {'courses' : all_courses } 
    return render(request,'root/streams.html',context)

@login_required(login_url="login")
def watchPage(request , stream_name):
    code = stream_name
    code = unquote(code)
    streams = Stream.objects.filter(stream_code=code)
    stream = streams.first()

    if stream is not None:
        context = {'stream' : stream , 'stream_link' : stream.stream_code} 
    else:
        context = {}

    return render(request,'root/watch.html',context)


@login_required(login_url="login")
def broadcastPage(request):
    form = StreamForm()

    if request.method == "POST":  
        if 'save_stream' in request.POST:      
            form = StreamForm(request.POST)
            if form.is_valid():
                stream = form.save(commit=False)
                stream.stream_key = secrets.token_hex(14) 
                stream.stream_code = secrets.token_urlsafe(8)
                stream.live = False
                save_video = request.POST.get('save_stream','')
                if(save_video==True):
                    course = Course.objects.filter(name=stream.course_name).first()
                    from datetime import datetime
                    date = datetime.today().strftime('%Y-%m-%d')
                    video = Video(video_name=stream.stream_name,teacher_name=stream.teacher_name,course=course,stream_key=stream.stream_key,video_code=stream.stream_code,date=date)
                    video.save()

                stream.save()
                print("Saved")
                return redirect('/broadcast/'+quote(stream.stream_code) +'/')
        elif 'save_course' in request.POST:
            course_name = request.POST.get('course_name','')
            link = request.POST.get('link','')
            course = Course(name=course_name,link=link)
            course.save()
            
    courses = Course.objects.all()
    context = {'courses' : courses , 'form' : form } 
    return render(request,'root/broadcast.html',context)

@login_required(login_url="login")
def showPage(request , stream_name):
    code = stream_name
    code = unquote(code)
    streams = Stream.objects.filter(stream_code=code)
    stream = streams.first()

    if request.method == "POST":
        stream_name = request.POST.get('stream_name','')
        teacher_name = request.POST.get('teacher_name','')
        course_name = request.POST.get('course_name','')
        stream.stream_name = stream_name
        stream.teacher_name = teacher_name
        stream.course_name = course_name
        stream.save(update_fields=["stream_name","teacher_name","course_name"])
   
    if stream is not None:
        courses = Course.objects.all()
        context = {'stream' : stream , 'stream_link' : stream.stream_code , 'courses' : courses } 
    else:
        context = {}


    return render(request,'root/show.html',context)

@login_required(login_url="login")
def profilePage(request):
    
    context = {}
    return render(request,'root/profile.html',context)   

@login_required(login_url="login")
def coursePage(request,course_name):
    course = Course.objects.filter(link=course_name).first()
    videos = course.video_set.all()
    context = {'course':course,'videos':videos}
    return render(request,'root/course.html',context)   

@login_required(login_url="login")
def videoPage(request,course_name,video_code):
    video = Video.objects.filter(video_code=video_code).first()
    context = {'video' : video}
    return render(request,'root/video.html',context)   


def ajax(request):
    stream_id = request.POST.get('stream_id', False)
    stream = Stream.objects.get(pk=stream_id)
    stream.live = not stream.live
    stream.save()
    print(stream.live)
    print(stream_id)
    return redirect('/')
        


def chatPage(request):
    return render(request, 'root/chat.html', {} )

def roomPage(request, room_name):
    return render(request, 'root/room.html', {
        'room_name': room_name
    })

#============== Utility functions ================

import string
import random

def key_generator(length):
  
    LETTERS = string.ascii_letters
    NUMBERS = string.digits  
    PUNCTUATION = string.punctuation  

    # create alphanumerical from string constants
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    random_password = random.choices(printable, k=length)
    random_password = ''.join(random_password)
    return random_password