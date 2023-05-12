from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.db import models


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars", default='default.svg')
    country = CountryField()
    background = models.ImageField(upload_to='backgrounds', null=True)
    about = models.TextField(max_length=500, null=True)


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images")
    tags = models.TextField(max_length=500, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, null=True)
    color = models.CharField(null=True, max_length=7)
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)

