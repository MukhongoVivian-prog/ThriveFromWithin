# core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50,unique=True)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=20)
    email = models.EmailField()
    work_environment = models.JSONField(default=list)
    challenges = models.JSONField(default=list)
    code = models.CharField(max_length=20)
    num_of_employees = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name   
    

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'ADMIN'),
        ('manager', 'MANAGER'),
        ('employee', 'EMPLOYEE'),
        ('therapist', 'THERAPIST'),
    )
<<<<<<< HEAD
    MOODS = (
        ('happy',"Happy"),
        ('neutral',"Neutral"),
        ('sad',"Sad"),
        ('angry',"Angry"),
        ('anxious',"Anxious"),
        ('tired',"Tired"),
        ('confused',"Confused")
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=None)
    mood = models.CharField(max_length=10, choices=MOODS, default="neutral")
    image = models.FileField(null=True,blank=True,default=None)
    is_anonymous = models.BooleanField(default=False)
    recieve_notification = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(default=1, blank=True)
    bio = models.TextField(default="",blank=True)
    title = models.CharField(max_length=100,default="",blank=True)
=======
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    company_name = models.CharField(max_length=255, blank=True, null=True)
>>>>>>> 16352f77fe86a09254118d02b60f43dc41edab2d

    def __str__(self):
        return f"{self.first_name} ({self.role})"


class Material(models.Model):
    OPTION = (
        ('podcast','Podcast'),
        ("webinar",'Webinar'),
        ("audio",'Audio'),
        ('guide',"Guide")
    )

    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    option = models.CharField(max_length=30, choices=OPTION, default="webinar")
    by = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField()
    description = models.TextField(default="", blank=True)
    file = models.FileField(null=True, blank=True, default=None)
    link = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
    
class Affirmation(models.Model):
    quote = models.TextField()
    by = models.CharField(max_length=100)

    def __str__(self):
        return self.quote

class Scene(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField()

    def __str__(self):
        return self.title

class Sound(models.Model):
    title = models.CharField(max_length=100)
    tag = models.CharField(max_length=10)
    picture = models.FileField()
    audio = models.FileField()

    def __str__(self):
        return self.title