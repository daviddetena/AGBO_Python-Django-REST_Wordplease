# -* encoding:utf-8 *-
from django.http import HttpResponseNotFound
from django.shortcuts import render
from blogs.models import Blog

# Vistas basadas en clases
from django.views.generic import View

# url /blogs/
class BlogsView(View):
    """
    Vista basada en clase para el listado de blogs. En este casi sólo por GET
    """
    def get(self, request):
        """
        Método que se encarga de mostrar el listado de blogs de la plataforma
        :param request: Objeto request de petición
        :return: Objeto HttpResponse con el html que se entregará al template
        """
        blogs = Blog.objects.all().order_by('-created_at')
        context = {
            # Traemos de la DB los 5 últimos blogs
            "blog_list": blogs[:5]
        }

        # Con el render hacemos que nos pinte la template indicada en el 2º param, que es un html
        return render(request, 'blogs/home.html', context)