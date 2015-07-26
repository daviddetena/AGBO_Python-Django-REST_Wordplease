#-*- coding: utf-8 -*-
from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    """
    Heredamos de ModelForm para que genere un formulario automágicamente a partir de nuestro modelo Post
    """

    class Meta:
        """
        En la clase meta definimos el modelo base para crear el formulario. Podemos indicarle también los
        campos que queremos que aparezcan en el formulario (fields), y los que no (exclude)
        """
        # Formulario para el modelo Post
        model = Post
        exclude = ['blog', 'published_at']        # excluimos el blog, ya que queremos que lo coja del usuario autenticado