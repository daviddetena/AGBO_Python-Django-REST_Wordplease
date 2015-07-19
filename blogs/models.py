# -* encoding:utf-8 *-
from django.db import models


# Create your models here.

class Post(models.Model):
    """
    Definimos el modelo Post. Como cada usuario tendrá un único blog en principio, hacemos que el usuario del post sea
    el usuario autenticado.
    """
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    body = models.TextField()
    imageUrl = models.URLField(blank=True, null=True, default="")   # Imagen url opcional
    created_at = models.DateTimeField(auto_now_add=True)            # Se guarda la fecha al crearse
    modified_at = models.DateTimeField(auto_now=True)               # Se actualiza cada vez que se guarde
    published_at = models.DateTimeField()

    def __unicode__(self):
        """
        Método especial privado que muestra la representación en cadena del objeto. El self no cuenta como parámetro
        """
        return self.title

class Tag(models.Model):
    """
    Definimos el modelo Category. Este indicará el nombre de la categoría. En una misma categoría podrá haber varios
    posts, y un mismo post puede estar en distintas categorías.
    """
    name = models.CharField(max_length=50)