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
from posts.views import HomeView, UserPostsView, DetailView, CreateView, ListView
from users.views import LoginView, LogoutView
from blogs.views import BlogsView

urlpatterns = [
    # (?P<pk>[0-9]+) => valor en parámetro pk (?P<pk>), que será 1 o más números del 0 al 9

    url(r'^admin/', include(admin.site.urls)),

    # urls nombradas
    url(r'^blogs/$', BlogsView.as_view(), name='blog_home'),    # listado de blogs, con vista basada en clase BlogsView
    url(r'^$', HomeView.as_view(), name='post_home'),           # listado de posts, con vista basada en clase HomeView
    url(r'^posts/$', ListView.as_view(), name='post_list'),    # post de usuario autenticado/todos los posts, basada en clase PostUserView
    url(r'^blogs/(?P<username>[a-z]+)/$', UserPostsView.as_view(), name='blog_posts'),     # listado posts blog usuario, basada en la clase UserPostView
    url(r'^blogs/(?P<username>[a-zA-Z]+)/(?P<post_id>[0-9]+)$', DetailView.as_view(), name='post_detail'),   # detalle post, basado en clase DetailView
    url(r'^login$', LoginView.as_view(), name='user_login'),    # login, con vista basada en clase LoginView
    url(r'^logout$', LogoutView.as_view(), name='user_logout'), # logout, con vista basada en clase LogoutView

    url(r'^new-post/$', CreateView.as_view(), name='post_create')   # creación nuevo post, con vista basada en clase CreateView
    #url(r'^.*$', '', name='url_not_found')                     # controlador para redirección a home
]
