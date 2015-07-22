# -* encoding:utf-8 *-
"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # (?P<pk>[0-9]+) => valor en parámetro pk (?P<pk>), que será 1 o más números del 0 al 9

    url(r'^admin/', include(admin.site.urls)),

    url(r'^blogs/$', 'blogs.views.home'),                                               # listado blogs plataforma
    url(r'^$', 'posts.views.home'),                                                     # listado posts plataforma
    #url(r'^posts/$', 'posts.views.home'),                                               # listado posts plataforma
    url(r'^blogs/(?P<username>[a-z]+)/$', 'posts.views.user_posts'),                    # listado posts blog usuario
    url(r'^blogs/(?P<username>[a-zA-Z]+)/(?P<post_id>[0-9]+)$', 'posts.views.detail')   # detalle post usuario
]
