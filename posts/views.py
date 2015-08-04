# -* encoding:utf-8 *-
from blogs.models import Blog
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from posts.forms import PostForm
from posts.models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator

#Todo: Ver todos los listados segun los queryset. Cambiar las clases según estos y heredar de ello.
# Convertimos nuestras vistas basadas en métodos en vistas basadas en clases.


class PostsQuerySet(object):

    """
    Definimos métodos para los querysets según permisos
    """
    def get_posts_queryset(self, request):
        """
        Definimos queryset de listado de posts, según permisos
        """

        if not request.user.is_authenticated():
            # Si no está autenticado => TODOS los PUBLICADOS
            posts = Post.objects.filter(published_at__isnull=False)
        elif request.user.is_superuser:
            # Admin => TODOS los posts
            posts = Post.objects.all()
        else:
            # No es admin y está autenticado => TODOS los de ese usuario, publicados o no, y los PUBLICOS del resto
            # COMPROBAR DESPUES, O CREAR UN GET_POSTS_BLOG_QUERYSET para el nombre de blog.
            posts = Post.objects.filter(Q(blog__owner=request.user) | Q(published_at__isnull=False))

        # Ordenamos resultados por fecha de publicación, o de creación
        return posts.order_by('-published_at', '-created_at')



    def get_post_detail_queryset(self, request, pk):
        """
        Definimos queryset para el detalle de post. Llamamos al método anterior, para que filtre por pk.
        """
        posts = self.get_posts_queryset(request).filter(pk=pk)

        if len(posts) == 1:
            return posts[0]
        else:
            return None


#url /
class HomeView(View):
    """
    Vista basada en clase para el home. Tendremos que definir los métodos del HTTP get y post. En este caso, es sólo por GET
    """
    def get(self, request):
        """
        Controlador que se muestra para el directorio raíz de la plataforma con los últimos posts publicados, sea de
        quien sea.
        :param request: Objeto request de la petición
        :return: Objeto HttpResponse con el código html que se entregará al usuario
        """
        # A través del object manager de clase <objects> obtenemos los objetos del modelo Post. Configura la query
        # Obtenemos todos los post publicados
        posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')

        # El context es lo que se le pasará al template, siendo las claves del diccionario accesibles desde ellas
        context = {
            # No carga en memoria todos los objetos, sino los 5 primeros. Aquí pondría el LIMIT X de SQL
            # Sólo en el momento en que la variable va a ser utilizada es traído de la DB
            "post_list": posts[:5]
        }

        # Con el render hacemos que nos pinte la template indicada en el 2º param, que es un html
        return render(request, 'posts/home.html', context)


# url /blogs/<nombre_usuario>/
class UserPostsView(View, PostsQuerySet):

    def get(self, request, username):
        """
        Método para manejar la vista en detalle de un blog. Queremos que se muestren todos los
        artículos de ese blog
        :param request: Objeto request con la petición
        :param pk: Parámetro pk con el identificador del blog cuyo detalle se mostrará
        :return: render que cargará la vista de detalle del blog (por debajo, crea un HttpResponse)
        """

        # OBTENER BLOG CUYO NAME = EL PARAMETRO. OBTENER POSTS DE ESE BLOG
        possible_blogs = Blog.objects.filter(owner__username__exact=username)

        if len(possible_blogs) == 1:
            # Del PostsQuerySet filtramos aquellos posts que sean del blog del usuario requerido
            possible_posts = self.get_posts_queryset(self.request).filter(blog__owner__username__exact=username)

            context = {
                "post_list": possible_posts
            }
            return render(request, 'posts/user_posts.html', context)
        else:
            # 404 - blog no encontrado
            return HttpResponseNotFound('No existe el blog')


# url /blogs/<nombre_usuario>/<post_id>
class DetailView(View, PostsQuerySet):
    """
    Vista basada en clase para el detalle de post. Tendremos que definir los métodos del HTTP get y post. En este caso, es sólo por GET
    """
    def get(self, request, username, post_id):
        """
        Método para manejar la vista detalle de un post.
        :param request: Objeto request con la petición
        :param pk: Parámetro pk con el identificador del blog cuyo detalle se mostrará
        :return: render que cargará la vista de detalle del post (por debajo, crea un HttpResponse)
        """

        # Obtenemos queryset del detalle de post
        possible_post = self.get_post_detail_queryset(self.request, post_id)
        if possible_post is not None:
            context = {
                "post": possible_post
            }
            # cargamos template con los datos del contexto, que incluye el post a mostrar
            return render(request, 'posts/detail.html', context)

        else:
            # error 404 - post no encontrado
            return HttpResponseNotFound('No existe el post')


# url /new_post/
class CreateView(View):
    """
    Vista basada en clase para el la creación de post. Tendremos que definir los métodos del HTTP get y post.
    """
    @method_decorator(login_required())
    def get(self, request):
        """
        Muestra un formulario para crear un post. Este formulario no se manda nunca por get, por lo que no es
        necesario incluir mensajes de error.
        :param request: Objeto HttpRequest con la petición
        :return: HttpResponse
        """

        # Formulario vacío si viene por GET
        form = PostForm()

        context = {
            'form': form,
            'success_message': ''
        }

        return self.renderize(request, context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Crea un post en base a la información POST. Con el decorador @login_required() nos va a ejecutar esta función
        solamente en el caso de que el usuario esté autenticado. En caso contrario, redirigirá a una url del paquete
        django.contrib.auth que redefinimos en el settings.py LOGIN_URL. Esta es la magia que hace Django para
        redireccionar al usuario a una url en el caso de que intente acceder a una url protegida sólo accesible si
        está autenticado.
        :param request: Objeto HttpRequest con la petición
        :return: HttpResponse
        """
        success_message = ''

        # Creo un post vacío y le asigno el blog actual.
        post_with_blog = Post()
        post_with_blog.blog = request.user.blog

        # Le pedimos al formulario que en vez de usar la instancia que él crea, utilice la que le
        # indicamos con el post_with_blog. Con esto, guarda la instancia con todos los campos del
        # formulario, excepto del blog, que coge el que le indicamos nosotros que ha sido creado.
        form = PostForm(request.POST, instance=post_with_blog)

        if form.is_valid():
            # Si se valida correctamente creamos objeto post, lo guardamos en DB y lo devolvemos
            # Obtenemos el blog del usuario autenticado para guardarlo automáticamente.
            new_post = form.save()

            # Reiniciamos formulario y componemos mensaje con enlace al nuevo post creado. Para acceder a una url
            # nombrada en un controlador utilizamos la función reverse, con los argumentos de la url nombrada, en este
            # caso, el nombre del blog, y la pk del post.
            # Como por defecto Django escapa el HTML, necesitamos indicar que el enlace al nuevo post no escape HTML.
            # Lo indicamos en la plantilla con el |safe en el mensaje. Lo normal es que este trabajo se haga en el
            # template
            form = PostForm()
            success_message = '¡Post creado con éxito!  '
            success_message += '<a href="{0}">'.format(reverse('post_detail', args=[new_post.blog, new_post.pk]))
            success_message += 'Ver post'
            success_message += '</a>'

        context = {
            'form': form,
            'success_message': success_message
        }

        return self.renderize(request, context)

    def renderize(self, request, context):
        """
        Cargamos template con los datos del contexto, que incluye el formulario basado en modelo
        En el template podemos incluir cada campo como <p>, <tr> de table o <li> de <ul>
        :param request: HttpRequest
        :param context: Contexto con los datos a los que el template tendrá acceso
        :return: render que genera el HttpResponse con el context y el template indicados
        """
        return render(request, 'posts/new_post.html', context)