#-*- coding: utf-8 -*-
from posts.models import Post
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from posts.serializers import PostSerializer, PostListSerializer


class PostListAPI(ListCreateAPIView):
    """
    Heredando de ListCreateAPIView de generics permitimos que REST nos automatice el listado y creación de post
    """
    queryset = Post.objects.all()

    def get_serializer_class(self):
        """
        Sobreescribimos esta clase para saber que serializer debo usar. Si es por POST necesitaremos todos los campos; si es un listado (GET), sólo los campos del PostListSerializer
        """
        return PostSerializer if self.request.method == "POST" else PostListSerializer



class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Heredando de RetrieveUpdateDestroyAPIView de generics permitimos que REST nos automatice el detalle, actualización y borrado de un post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer