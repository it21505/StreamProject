from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_auth_ldap.backend import LDAPBackend

class Profile(models.Model):
    STUDENT = 1
    TEACHER = 2
    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return self.user.username

    def create_student_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = Profile.objects.create(user=instance)
            user = LDAPBackend().populate_user(instance.username)
            if user:
                fname = user.ldap_user.attrs.get("givenName", [])[0]
                lname = user.ldap_user.attrs.get("sn", [])[0]
                title = user.ldap_user.attrs.get("title", [])[0]
                department = user.ldap_user.attrs.get("schacPersonalPosition", [])[0]

                if 'Καθηγητής' in title or 'Διδάκτωρ' in title or 'Συνεργάτης' in title:
                    title = 2
                else:
                    title = 1
                
                if 'Πληροφορικής' in department:
                    department = "Informatics and Telematics"
                elif 'Οικονομίας' in department:
                    department = "Economics and Sustainable Development"
                elif 'Επιστήμης Διαιτολογίας-Διατροφής' in department:
                    department = "Nutrition and Dietetics"
                elif 'Γεωγραφίας' in department:
                    department = "Geography"
                else:
                    department = ""

                new_profile.first_name = fname
                new_profile.last_name = lname
                new_profile.department = department
                new_profile.role = title
                new_profile.save()
        
    post_save.connect(create_student_profile, sender=User)


class Course(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


