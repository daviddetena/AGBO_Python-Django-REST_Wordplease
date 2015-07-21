# -* encoding:utf-8 *-
from django.db import models


class Category(models.Model):
    """
    Definimos modelo Category. Varios posts pueden estar en una misma categoría, y un mismo post tener varias
    categorías.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name