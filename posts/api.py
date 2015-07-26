#-*- coding: utf-8 -*-
from posts.models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from posts.serializers import PostSerializer

class PostListAPI(APIView):

    def get(self, request):
        """
        Endpoint de listado de posts. Devuelve
        :param request:
        :return:
        """
        # Recuperamos todos los posts de la base de datos
        posts = Post.objects.all()

        # El serializador por defecto serializa un objeto. Tenemos que indicarle que serialice
        # todos los posts recibidos, poniendo many=True.
        # El serializador se guarda los datos en data
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)