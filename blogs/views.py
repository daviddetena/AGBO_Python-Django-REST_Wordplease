# -* encoding:utf-8 *-
from django.shortcuts import render
from blogs.models import Blog

# TODO: crear las siguientes views-templates:
# /blogs/                               => listado de blogs de usuarios
# /blogs/<nombre_usuario>               => posts usuario, más recientes primero
# /blogs/<nombre_usuario>/<post_id>     => vista detalle post: titulo, resumen, cuerpo, url imagen,
#                                          fecha publicacion, categorías

def home(request):
    """
    Controlador que se encarga de mostrar contenido en la url /blogs/ de la plataforma
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
