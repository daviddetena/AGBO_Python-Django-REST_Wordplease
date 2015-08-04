# -* encoding:utf-8 *-
from django.contrib import admin
from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    """

    """
    # Lista de columnas que se verán en el admin. Para el blog llamamos a método que me devuelve el nombre y apellidos del usuario propietario del blog
    list_display = ('title', 'summary', 'blog_owner_name', 'created_at', 'published_at')

    # Lista de filtros que aparecerán a la derecha
    list_filter = ('blog', 'categories')

    # Lista de parámetros por los que se podrá buscar
    search_fields = ('title', 'summary', 'body')


    def blog_owner_name(self, obj):
        """
        Método que altera el campo list_display blog para poner el nombre y apellidos del propietario del blog del post
        :param obj:
        :return:
        """
        return obj.blog.owner.first_name + u' ' + obj.blog.owner.last_name

    # Atributos a métodos de función blog_owner_name, para poder indicar el header de columna y el campo correspondiente por el que ordena
    blog_owner_name.short_description = u'Blog owner'
    blog_owner_name.admin_order_field = 'blog'


    # Definimos campos que aparecen en la vista detalle del Post en el admin
    fieldsets = (
        ('General', {
            'fields': ('title', 'summary', 'body'),
            'classes': ('wide',)
        }),
        ('Addional info',{
            'fields': ('imageUrl', 'blog', 'categories'),
            'classes': ('wide',)
        })
    )



# Registramos modelo Post, manejado por nuestra clase PostAdmin
admin.site.register(Post, PostAdmin)
