#-*- coding: utf-8 -*-
# Importamos settings del proyecto
from django.conf import settings

# Si no hay PROJECT_BADWORDS en el settings no incluimos ningún badwords
BADWORDS = getattr(settings, 'PROJECT_BADWORDS', [])
