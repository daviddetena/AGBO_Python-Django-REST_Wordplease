# -* encoding:utf-8 *-
from django.conf import settings
from django.db import models


# Create your models here.

class Blog(models.Model):
    """
    Definimos el modelo Blog
    """
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)        # Se guarda con la fecha y hora actuales al crearse
    modified_at = models.DateTimeField(auto_now=True)           # Se actualiza cada vez que se guarde
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

class Post(models.Model):
    """
    Definimos el modelo Post
    """
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    body = models.TextField()
    imageUrl = models.URLField(blank=True, null=True, default="")   # Imagen url opcional
    created_at = models.DateTimeField(auto_now_add=True)            # Se guarda la fecha al crearse
    modified_at = models.DateTimeField(auto_now=True)               # Se actualiza cada vez que se guarde
    published_at = models.DateTimeField()