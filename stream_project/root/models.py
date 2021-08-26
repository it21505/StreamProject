from django.db import models
from accounts.models import Course
# Create your models here.

class Stream(models.Model):
    stream_name = models.CharField(max_length=200)
    teacher_name = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    stream_key = models.CharField(max_length=200)
    stream_code = models.CharField(max_length=200)
    save_stream = models.BooleanField()
    live = models.BooleanField()
    

    def __str__(self):
        return self.stream_name

class Video(models.Model):
    video_name = models.CharField(max_length=200)
    teacher_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,null=True)
    stream_key = models.CharField(max_length=200,primary_key=True)
    video_code = models.CharField(max_length=200)
    date = models.DateField()
    

    def __str__(self):
        return self.video_name