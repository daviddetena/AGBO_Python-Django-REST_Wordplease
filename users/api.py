#-*- coding: utf-8 -*-
from blogs.models import Blog
from django.contrib.auth.models import User
from rest_framework.views import APIView
from users.serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

class UserListAPI(APIView):
    """
    Vista basada en clase para el listado de Users de la API Rest. En este caso, sólo se accede por GET.
    Las APIView nos proporciona un API rest navegable.
    """

    def get(self, request):
        """
        Endpoint de listado de usuarios. Devuelve en formato JSON una lista de diccionarios con los datos de cada usuario.
        :param request:
        :return:
        """
        users = User.objects.all()      # Obtenemos todos los usuarios

        # El serializador por defecto serializa un objeto. Tenemos que indicarle que serialice
        # todos los usuarios recibidos, poniendo many=True.
        # El serializador se guarda los datos en users.data, transformándolo en una lista de
        # diccionarios, con JSONRenderer
        serializer = UserSerializer(users, many=True)

        # Con las clases APIView de REST framework automágicamente me hace la conversión de JSON, XML
        # a diccionarios, y viceversa, y sólo trabajamos con el DATA del serializer
        return Response(serializer.data)

    def post(self, request):
        """
        Endpoint de creación de usuario. Por convención, se utiliza la url de listado con una petición POST para la creación de un objeto de ese listado. En el serializer.save() comprueba automáticamente si tiene instasncia del User; si no la tiene, llama al método create del serializer.
        """

        # Creamos serializador a partir de los datos de la petición. En rest framwork, para evitar request.POST,
        # request.GET, etc., se utiliza simplemente data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Guardamos el usuario a través del serializer y devolvemos los datos del objeto creado
            new_user = serializer.save()

            # Guardamos blog para el nuevo usuario
            user_blog = Blog()
            user_blog.owner = new_user
            user_blog.save()

            # Respondemos código 201 (creado) y los datos del objeto creado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Devolvemos diccionario con errores y el código 400 (petición errónea) si algo fue mal
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPI(APIView):
    """
    Vista basada en clase para el detalle de User.
    """
    def get(self, request, pk):
        """
        Endpoint detalle de usuario
        :param request:
        :return:
        """
        # Si existe el usuario cuya PK=pk existe lo devuelve, y si no se captura una excepción y se manda
        # un código 404
        # La función get_object_or_404 recibe el modelo como primer parámetro y a continuación los campos
        # de búsqueda
        user = get_object_or_404(User, pk=pk)

        # Convertimos objeto user en diccionario, que es guardado en 'data'
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request, pk):
        """
        Endpoint de modificación de usuario. Por convención, se utiliza la url de listado con una petición PUT para la modificación de un objeto de ese listado. En el serializer.save() comprueba automáticamente si tiene instasncia del User; si la tiene, coge esa instancia y llama al update() del serializer; si no la tiene, llama al método create() del serializer, como en el caso del POST del UserListAPI
        """
        user = get_object_or_404(User, pk=pk)
        # Actualiza los datos de la instancia recuperada con los datos que me pasan por la API
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)