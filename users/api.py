#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.views import APIView
from users.serializers import UserSerializer
from rest_framework.response import Response

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

