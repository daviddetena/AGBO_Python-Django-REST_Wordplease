# -* encoding:utf-8 *-
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

# url /login/
from users.forms import LoginForm


def login(request):
    """
    Controlador para el login de usuario
    :param request: Objeto request de la petición
    :return: HttpResponse con el código html que se entregará al usuario
    """
    # Mensajes de error al autenticar
    error_messages = []

    if request.method == "POST":

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
                    # Redirigir al home
                    return redirect('post_home')
                else:
                    error_messages.append('El usuario no está activo')
    else:
        # GET, no existe. Form vacío
        form = LoginForm()

    # Creamos contexto con los mensajes de error
    context = {
        'errors': error_messages,
        'login_form': form
    }

    # Mandamos respuesta con error a través de la plantilla
    return render(request, 'users/login.html', context)


# url /logout/
def logout(request):
    """
    Controlador para el logout de usuario (lo hace Django)
    :param request: Objeto request de la petición
    :return: HttpResponse con el código html que se entregará al usuario
    """
    # Desautenticar usuario y redirigir al home
    if request.user.is_authenticated():
        django_logout(request)
    # Redirige a la url de name='post_home'
    return redirect('post_home')

