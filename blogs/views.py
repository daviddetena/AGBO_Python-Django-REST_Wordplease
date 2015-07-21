# -* encoding:utf-8 *-
from django.http import HttpResponseNotFound
from django.shortcuts import render
from blogs.models import Blog

# TODO: crear las siguientes views-templates:
# /blogs/<nombre_usuario>/<post_id>     => vista detalle post: titulo, resumen, cuerpo, url imagen,
#                                          fecha publicacion, categorías
from posts.models import Post

# url /blogs/
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

# url /blogs/<blog_id>
def detail(request, pk):
    """
    Controlador para manejar la vista en detalle de un blog. Queremos que se muestren todos los
    artículos de ese blog
    :param request: Objeto request con la petición
    :param pk: Parámetro pk con el identificador del blog cuyo detalle se mostrará
    :return: render que cargará la vista de detalle del blog (por debajo, crea un HttpResponse)
    """

    # Buscamos Blog con primary key = a la del parámetro
    possible_blogs = Blog.objects.filter(owner=pk)
    blog = possible_blogs[0] if len(possible_blogs) >= 1 else None

    if blog is not None:
        # cargar plantilla detalle blog con el listado de blogs
        posts = Post.objects.filter(blog=pk).order_by('-created_at')
        context = {
            # Devolvemos blog y posts
            "blog": blog,
            "post_list": posts      # ver cuántos se incluyen
        }
        return render(request, 'blogs/detail.html', context)
    else:
        # 404 - no existe el blog con ese pk
        return HttpResponseNotFound('No existe el blog')
