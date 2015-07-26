#-*- coding: utf-8 -*-
from posts.models import Post
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from posts.serializers import PostSerializer


class PostListAPI(ListCreateAPIView):
    """
    Heredando de ListCreateAPIView de generics permitimos que REST nos automatice el listado y creación de post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Heredando de RetrieveUpdateDestroyAPIView de generics permitimos que REST nos automatice el detalle, actualización y borrado de un post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer