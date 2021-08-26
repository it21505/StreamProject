from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.indexPage, name='index'),
    path('streams/', views.streamsPage, name='streams'),
    path('streams/<str:stream_name>/', views.watchPage , name='watch'),
    path('contact/', views.contactPage , name='contact'),
    path('broadcast/', views.broadcastPage , name='broadcast'),
    path('broadcast/<str:stream_name>/', views.showPage , name='show'),
    path('profile/', views.profilePage , name='profile'),
    path('courses/<str:course_name>/', views.coursePage , name='course'),
    path('courses/<str:course_name>/<str:video_code>/', views.videoPage , name='video'),
    path('ajax/', views.ajax, name='ajax'), 

    path('chat/',views.chatPage , name='chat'),
    path('chat/<str:room_name>/', views.roomPage, name='room'),
]