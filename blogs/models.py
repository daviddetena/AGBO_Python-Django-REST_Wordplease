# -* encoding:utf-8 *-
from django.contrib.auth.models import User
from django.db import models

class Blog(models.Model):
    """
    Definimos el modelo Blog. Un blog será creado automáticamente al registrarse un nuevo usuario. El
    nombre del blog será el nombre de usuario del nuevo usuario registrado.
    """
    owner = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)        # Se guarda al crearse el blog

    def __unicode__(self):
        """
        Método especial privado que muestra la representación en cadena del objeto. El self no cuenta como parámetro
        """
        return self.owner.username