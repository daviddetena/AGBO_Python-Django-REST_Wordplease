#-*- coding: utf-8 -*-
from blogs.models import Blog
from rest_framework.generics import ListAPIView
from blogs.serializers import BlogSerializer

class BlogListAPI(ListAPIView):
    """
    Heredando de ListAPIView de generics permitimos que REST nos automatice el listado de blogs
    """
    queryset = Blog.objects.all().order_by('owner__username')
    serializer_class = BlogSerializer
