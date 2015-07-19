# -* encoding:utf-8 *-
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from blogs.models import Post

# Create your views here.

def home(request):
    """
    Vista que se muestra para el directorio raíz de la plataforma
    :param request: Método con el objeto request de la petición
    :return: HttpReponse con el código html que se entregará al usuario
    """
    posts = Post.objects.all()
    html = '<ul>'
    for post in posts:
        html += '<li>' + post.title + '</li>'
    html += '</ul>'
    return HttpResponse(html)