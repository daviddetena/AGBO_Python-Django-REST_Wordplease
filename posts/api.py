#-*- coding: utf-8 -*-
from posts.models import Post
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posts.serializers import PostSerializer, PostListSerializer


class PostListAPI(ListCreateAPIView):
    """
    Heredando de ListCreateAPIView de generics permitimos que REST nos automatice el listado y creación de post
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)      # Sólo lectura para no autenticados.

    def get_serializer_class(self):
        """
        Sobreescribimos esta clase para saber que serializer debo usar. Si es por POST necesitaremos todos los campos;
        si es un listado (GET), sólo los campos del PostListSerializer
        """
        return PostSerializer if self.request.method == "POST" else PostListSerializer

    def get_queryset(self):
        """
        Definimos los datos a mostrar según el usuario, redefiniendo el get_queryset del GenericView
        """
        if self.request.user.is_authenticated():
            if self.request.user.is_superuser:
                # Admin ve todos, publicados o no
                posts = Post.objects.all().order_by('-published_at')
            else:
                # Usuario autenticado. Ve todos sus posts, publicados o no
                posts = Post.objects.filter(blog=self.request.user.blog).order_by('-published_at')
        else:
            # Usuarios no autenticados - Sólo posts públicos
            posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
        return posts

    def perform_create(self, serializer):
        """
        Indicamos que el campo blog del objeto post sea el blog del usuario autenticado
        """
        serializer.save(blog=self.request.user.blog)



class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Heredando de RetrieveUpdateDestroyAPIView de generics permitimos que REST nos automatice el detalle,
    actualización y borrado de un post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)      # Sólo lectura para no autenticados.