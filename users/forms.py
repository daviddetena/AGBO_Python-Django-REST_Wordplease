#-*- coding: utf-8 -*-
from django import forms

class LoginForm(forms.Form):
    """
    Definimos nuestra clase LoginForm para crear un formulario de Django con los campos que le indicamos
    """
    # campos, siempre tienen que heredar de XXXField
    # Con widget indicamos de qué tipo queremos que pinte el campo
    usr = forms.CharField(label="Nombre de usuario")
    pwd = forms.CharField(label="Contraseña", widget=forms.PasswordInput())

