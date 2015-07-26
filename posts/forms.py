#-*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from posts.models import Post
from posts.settings import BADWORDS


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
        exclude = ['blog','published_at']        # excluimos el blog, ya que queremos que lo coja del usuario autenticado

    def clean(self):
        """
        Valida si en el resumen y cuerpo del post se han puesto tacos definidos en settings.BADWORDS
        :return: diccionario con los atributos del formulario si OK
        """
        cleaned_data = super(PostForm, self).clean()    # clase padre limpia campos
        # obtenemos summary y body o cadenas vacías
        summary = cleaned_data.get('summary', '')
        body = cleaned_data.get('body', '')

        # recorremos la lista de palabras prohibidas y si en el campo summary y body del formulario se encuentra alguna de ellas, lanzamos excepción. Esta excepción hará que se muestre el correspondiente mensaje de error en la pantalla
        for badword in BADWORDS:

            if badword.lower() in summary.lower():
                raise ValidationError(u'La palabra {0} no está permitida'.format(badword))

            if badword.lower() in body.lower():
                raise ValidationError(u'La palabra {0} no está permitida'.format(badword))

        # Si la cosa va bien, devuelvo los datos limpios/normalizados
        return cleaned_data