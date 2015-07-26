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
        read_only_fields = ('blog',)

class PostListSerializer(PostSerializer):
    """
    Utilizamos otra clase de serializer para que el listado muestre otros campos distintos a los por defecto
    """
    class Meta(PostSerializer.Meta):
        """
        Heredamos de PostSerializer.Meta para que sepa qué model es
        """
        fields = ('title', 'imageUrl', 'summary', 'published_at')