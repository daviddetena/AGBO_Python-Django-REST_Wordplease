#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View
from users.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer

class UserListAPI(View):
    """
    Vista basada en clase para el listado de Users de la API Rest. En este caso, sólo se accede por GET
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
        serialized_users = serializer.data
        renderer = JSONRenderer()

        # lista de diccionarios -> JSON
        json_users = renderer.render(serialized_users)

        return HttpResponse(json_users)

