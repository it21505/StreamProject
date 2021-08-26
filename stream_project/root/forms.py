
from django import forms
from .models import Stream
from accounts.models import Course

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

class StreamForm(forms.ModelForm):
    course_name = forms.ModelChoiceField(queryset=Course.objects.all(), to_field_name="name")
    course_name.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Stream
        fields = ['stream_name' , 'teacher_name' , 'course_name' , 'save_stream']
        widgets = {
            'stream_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Stream Name'}),
            'teacher_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Teacher Name'}),
            'save_stream': forms.Select(choices=TRUE_FALSE_CHOICES,attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [ 'name' , 'link' ]
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control','placeholder': 'Course Name'}),
            'link' : forms.TextInput(attrs={'class': 'form-control','placeholder': 'Course Link'}),
        }