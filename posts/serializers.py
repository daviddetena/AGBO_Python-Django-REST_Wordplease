#-*- coding: utf-8 -*-
from rest_framework import serializers
from models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Heredamos de ModelSerializer para ahorrarnos operaciones
    """
    class Meta:
        """
        Indicamos con model que el serializer está basado en el modelo Post
        """
        model = Post