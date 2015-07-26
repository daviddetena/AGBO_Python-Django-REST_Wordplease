#-*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from posts.settings import BADWORDS


def badwords_detector(value):
    """
    Valida si en value se han incluido tacos definidos en settings.BADWORDS
    :param value:
    :return: Boolean
    """

    # recorremos la lista de palabras prohibidas y si se encuentra en él value, devolvemos error
    for badword in BADWORDS:
        if badword.lower() in value:
            raise ValidationError(u'La palabra {0} no está permitida'.format(badword))

    # Si la cosa va bien, devuelvo True
    return True