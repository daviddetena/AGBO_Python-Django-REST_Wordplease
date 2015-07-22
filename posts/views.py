# -* encoding:utf-8 *-
from blogs.models import Blog
from django.http import HttpResponseNotFound
from django.shortcuts import render
from posts.models import Post

# TODO: crear las siguientes views-templates:
# /new_post           => Formulario nuevo post. Autenticación requerida. Usuario a partir de autenticación.

#url / o /posts/
def home(request):
    """
    Controlador que se muestra para el directorio raíz de la plataforma con los últimos posts
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


# url /blogs/<nombre_usuario>/
def user_posts(request, username):
    """
    Controlador para manejar la vista en detalle de un blog. Queremos que se muestren todos los
    artículos de ese blog
    :param request: Objeto request con la petición
    :param pk: Parámetro pk con el identificador del blog cuyo detalle se mostrará
    :return: render que cargará la vista de detalle del blog (por debajo, crea un HttpResponse)
    """

    # OBTENER BLOG CUYO NAME = EL PARAMETRO. OBTENER POSTS DE ESE BLOG
    possible_blogs = Blog.objects.filter(owner__username=username).order_by('-created_at')
    blog = possible_blogs[0] if len(possible_blogs) >=1 else None

    if blog is not None:
        # Recuperar posts de ese blog
        posts = Post.objects.filter(blog__owner__username=username).order_by('-created_at')
        context = {
            "post_list": posts
        }
        return render(request, 'posts/user_posts.html', context)
    else:
        # 404 - blog no encontrado
        return HttpResponseNotFound('No existe el blog')


# url /blogs/<nombre_usuario>/<post_id>
def detail(request, username, post_id):
    """
    Controlador para manejar la vista detalle de un post.
    :param request: Objeto request con la petición
    :param pk: Parámetro pk con el identificador del blog cuyo detalle se mostrará
    :return: render que cargará la vista de detalle del post (por debajo, crea un HttpResponse)
    """

    # OBTENER BLOG CUYO NAME = EL PARAMETRO. OBTENER POSTS DE ESE BLOG
    possible_blogs = Blog.objects.filter(owner__username=username)
    blog = possible_blogs[0] if len(possible_blogs) >=1 else None

    if blog is not None:
        # Recuperar post de ese blog
        possible_posts = Post.objects.filter(blog__owner__username=username, pk=post_id)
        post = possible_posts[0] if len(possible_posts) >=1 else None

        if post is not None:
            # Contexto con post a mostrar
            context = {
                "post": post
            }

            # cargamos template con los datos del contexto, que incluye el post a mostrar
            return render(request, 'posts/detail.html', context)
        else:
            # error 404 - post no encontrado
            return HttpResponseNotFound('No existe el post')
    else:
        # error 404 - blog no encontrado
        return HttpResponseNotFound('No existe el blog')



