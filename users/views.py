# -* encoding:utf-8 *-
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

# url /login/
def login(request):
    """
    Controlador para el login de usuario
    :param request: Objeto request de la petición
    :return: HttpResponse con el código html que se entregará al usuario
    """
    # Mensajes de error al autenticar
    error_messages = []

    if request.method == "POST":
        # Recuperar nombre de usuario y password del formulario
        username = request.POST.get('usr')
        password = request.POST.get('pwd')

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

    # Creamos contexto con los mensajes de error
    context = {
        'errors': error_messages
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

