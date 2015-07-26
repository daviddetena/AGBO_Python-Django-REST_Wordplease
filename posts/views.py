# -* encoding:utf-8 *-
from blogs.models import Blog
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from posts.forms import PostForm
from posts.models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator


# Convertimos nuestras vistas basadas en métodos en vistas basadas en clases.

#url /
class HomeView(View):
    """
    Vista basada en clase para el home. Tendremos que definir los métodos del HTTP get y post. En este caso, es sólo por GET
    """
    def get(self, request):
        """
        Controlador que se muestra para el directorio raíz de la plataforma con los últimos posts
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
            "post_list": posts
        }

        # Con el render hacemos que nos pinte la template indicada en el 2º param, que es un html
        return render(request, 'posts/home.html', context)


# url /blogs/<nombre_usuario>/
class UserPostsView(View):

    def get(self, request, username):
        """
        Método para manejar la vista en detalle de un blog. Queremos que se muestren todos los
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

            if request.user.is_authenticated():
                # Usuario autenticado. Admin y propietario ven todos, publicados o no. No propietario, sólo publicados
                if blog.owner == request.user or request.user.is_superuser:
                    posts = Post.objects.filter(blog=blog).order_by('-created_at')
                else:
                    posts = Post.objects.filter(blog=blog, published_at__isnull=False).order_by('-published_at')
            else:
                posts = Post.objects.filter(blog=blog, published_at__isnull=False).order_by('-published_at')

            context = {
                "post_list": posts
            }

            return render(request, 'posts/user_posts.html', context)
        else:
            # 404 - blog no encontrado
            return HttpResponseNotFound('No existe el blog')


# url /blogs/<nombre_usuario>/<post_id>
class DetailView(View):
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

        # OBTENER BLOG CUYO NAME = EL PARAMETRO. OBTENER POSTS DE ESE BLOG
        possible_blogs = Blog.objects.filter(owner__username=username)
        blog = possible_blogs[0] if len(possible_blogs) >=1 else None

        if blog is not None:
            # Recuperar post de ese blog. Nos traemos también su campo relacionado de blog (FK), para que los
            # haga en un único query. Prefetch_related para 1-n (1 post-n categorías)

            possible_posts = Post.objects.filter(blog__owner__username=username, pk=post_id).select_related('blog')
            post = possible_posts[0] if len(possible_posts) ==1 else None

            if post is not None:

                if request.user.is_authenticated():
                    # Usuario autenticado. Admin y propietario pueden verlo
                    if blog.owner == request.user or request.user.is_superuser:
                        context = {
                            "post": post
                        }
                    else:
                        if post.published_at is not None:
                            context = {
                                "post": post
                            }
                        else:
                            # error 403 - Acceso denegado
                            return HttpResponseForbidden('Acceso denegado')
                else:
                    if post.published_at is not None:
                        context = {
                            "post": post
                        }
                    else:
                        # error 403 - Acceso denegado
                        return HttpResponseForbidden('Acceso denegado')

                # cargamos template con los datos del contexto, que incluye el post a mostrar
                return render(request, 'posts/detail.html', context)
            else:
                # error 404 - post no encontrado
                return HttpResponseNotFound('No existe el post')
        else:
            # error 404 - blog no encontrado
            return HttpResponseNotFound('No existe el blog')


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


# url /posts/
class ListView(View):
    """
    Vista basada en clase para listado de post. Sólo tendremos peticiones por GET.
    """
    def get(self, request):
        """
        Devuelve igual que blogs/:
        - Si el usuario está autenticado o es administrador, todos los post del usuario autenticado, publicados o no.
        - Posts publicados del usuario, si no se está autenticado.
        Más recientes primero
        :param request: HttpRequest
        :return: render que genera el HttpResponse con el context y el template indicados
        """
        if request.user.is_authenticated() or request.user.is_superuser:
            # Usuario autenticado. Ve todos sus posts, publicados o no
            posts = Post.objects.filter(blog=request.user.blog).order_by('-created_at')
        else:
            # Usuarios no autenticados - Sólo posts públicos
            posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')

        context = {
            "post_list": posts
        }

        return render(request, 'posts/post_list.html', context)