#-*- coding: utf-8 -*-
from rest_framework import serializers
from models import Blog


class BlogSerializer(serializers.ModelSerializer):
    """
    Heredamos de ModelSerializer para ahorrarnos operaciones
    """
    class Meta:
        """
        Indicamos con model que el serializer está basado en el modelo Blog
        """
        model = Blog
