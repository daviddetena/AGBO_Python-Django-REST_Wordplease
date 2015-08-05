#-*- coding: utf-8 -*-
from posts.models import Post
from posts.views import PostsQuerySet
from posts.serializers import PostSerializer, PostListSerializer
from posts.permissions import PostPermissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class PostListAPI(PostsQuerySet, ListCreateAPIView):
    """
    Heredando de ListCreateAPIView de generics permitimos que REST nos automatice el listado y creación de post.
    GET: obtiene listado de post, utilizamos PostListSerializer.
    POST: creamos nuevo post para el blog actual, si se puede.
    """
    #permission_classes = (IsAuthenticatedOrReadOnly,)      # Sólo lectura para no autenticados.
    queryset = Post.objects.all()
    permission_classes = PostPermissions

    def get_serializer_class(self):
        """
        Sobreescribimos esta clase para saber que serializer debo usar. Si es por POST necesitaremos todos los campos;
        si es un listado (GET), sólo los campos del PostListSerializer
        """
        return PostSerializer if self.request.method == "POST" else PostListSerializer

    def get_queryset(self):
        """
        Heredamos del queryset de posts/views.py para el listado de posts
        """
        return self.get_posts_blog_queryset(self.request, self.request.user.username)

    def perform_create(self, serializer):
        """
        Indicamos que el campo blog del objeto post sea el blog del usuario autenticado
        """
        serializer.save(blog=self.request.user.blog)



class PostDetailAPI(PostsQuerySet, RetrieveUpdateDestroyAPIView):
    """
    Heredando de RetrieveUpdateDestroyAPIView de generics permitimos que REST nos automatice el detalle, actualización y borrado de un post.
    GET: detalle de post.
    PUT: actualización de post.
    DELETE: eliminación de post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = PostPermissions

    def get_queryset(self):
        """
        Heredamos del queryset de posts/views.py para el detalle de post
        """
        return self.get_posts_queryset(self.request)
