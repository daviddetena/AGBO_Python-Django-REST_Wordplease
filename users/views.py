# -* encoding:utf-8 *-
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
# url /login/
from users.forms import LoginForm
# Para vistas basadas en clases
from django.views.generic import View


# url /
class LoginView(View):
    """
    Vista basada en clase para el login. Tendremos que definir los métodos del HTTP get y post
    """

    def get(self, request):
        """
        Método para cuando el login viene del método HTTP get
        :param request: HttpRequest
        :return: render que contruye un HttpResponse con el template indicado
        """
        # Mensajes de error al autenticar
        error_messages = []

        form = LoginForm()

        # Creamos contexto con los mensajes de error
        context = {
            'errors': error_messages,
            'login_form': form
        }

        # Mandamos respuesta con error a través de la plantilla
        return render(request, 'users/login.html', context)

    def post(self, request):
        """
        Método para cuando el login viene del método HTTP get
        :param request: HttpRquest
        :return: render que contruye un HttpResponse con el template indicado
        """

        # Mensajes de error al autenticar
        error_messages = []

        # Crearemos un Django Form para presentarlo en la plantilla
        # Todos los valores del formulario se inicializan con los valores que vienen en el POST
        form = LoginForm(request.POST)

        # Si el formulario es válido, recuperamos datos
        if form.is_valid():

            # Recuperamos datos de formulario limpiados
            username = form.cleaned_data.get('usr')
            password = form.cleaned_data.get('pwd')

            # Con este método authenticate, Django automáticamente comprueba la autenticación del usuario,
            # haciendo las operaciones necesarias con la contraseña
            user = authenticate(username=username, password=password)

            if user is None:
                error_messages.append('Nombre de usuario o contraseña incorrectos')
            else:
                # El usuario debe estar activo
                if user.is_active:
                    # Autenticamos
                    django_login(request, user)

                    # Al autenticar, redirigir a la url que se indique en el parámetro next, o al home si no existe next
                    url = request.GET.get('next', 'post_home')
                    return redirect(url)
                else:
                    error_messages.append('El usuario no está activo')

        # Creamos contexto con los mensajes de error
        context = {
            'errors': error_messages,
            'login_form': form
        }

        # Mandamos respuesta con error a través de la plantilla
        return render(request, 'users/login.html', context)


# url /logout/
class LogoutView(View):
    """
    Vista basada en clase para el logout. Tendremos que definir los métodos del HTTP get y post
    """

    def get(self, request):
        """
        Método para logout. La desauntenticación la hace Django. El logout siempre va por GET
        :param request: HttpRequest
        :return: render que contruye un HttpResponse con el template indicado

        """
        # Desautenticar usuario y redirigir al home
        if request.user.is_authenticated():
            django_logout(request)
        # Redirige a la url de name='post_home'
        return redirect('post_home')

