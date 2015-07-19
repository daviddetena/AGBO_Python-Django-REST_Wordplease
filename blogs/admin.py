# -*- coding: utf-8 -*-
from blogs.models import Tag, Post
from django.contrib import admin

# Register my models for Admin UI
admin.site.register(Tag)
admin.site.register(Post)
