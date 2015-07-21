# -* encoding:utf-8 *-
from django.shortcuts import render
from posts.models import Post

# TODO: crear las siguientes views-templates:
# /new_post           => Formulario nuevo post. Autenticación requerida. Usuario a partir de autenticación.

def home(request):
    """
    Controlador que se muestra para el directorio raíz de la plataforma
    :param request: Objeto request de la petición
    :return: Objeco HttpResponse con el código html que se entregará al usuario
    """
    # A través del object manager de clase <objects> obtenemos los objetos del modelo Post. Configura la query
    posts = Post.objects.all().order_by('-created_at')

    # El context es lo que se le pasará al template, siendo las claves del diccionario accesibles desde ellas
    context = {
        # No carga en memoria todos los objetos, sino los 5 primeros. Aquí pondría el LIMIT X de SQL
        # Sólo en el momento en que la variable va a ser utilizada es traído de la DB
        "post_list": posts[:5]
    }

    # Con el render hacemos que nos pinte la template indicada en el 2º param, que es un html
    return render(request, 'posts/home.html', context)
