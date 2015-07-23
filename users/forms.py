#-*- coding: utf-8 -*-
from django import forms

class LoginForm(forms.Form):
    # campos, siempre tienen que heredar de XXXField
    # Con widget indicamos de qué tipo queremos que pinte el campo
    usr = forms.CharField(label="Nombre de usuario")
    pwd = forms.CharField(label="Contraseña", widget=forms.PasswordInput())

