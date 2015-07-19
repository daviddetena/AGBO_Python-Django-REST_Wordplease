# -* encoding:utf-8 *-
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Vista que se muestra para el directorio raíz de la plataforma
    :param request:
    :return:
    """
    return HttpResponse("Hola Mundo")
