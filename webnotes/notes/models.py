from django.db import models
from datetime import datetime

# Create your models here.

class Note(models.Model):
    user = models.CharField('Пользователь',  max_length=100, blank=False)
    name = models.CharField('Название заметки', max_length=100, blank=True)
    text = models.TextField('Текст заметки', max_length=1000, blank=True)
    favourites = models.BooleanField('Добавить в избранное', default=False, blank=True)
    date_update = models.DateTimeField('Дата последнего изменения', auto_now=True)
    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    date_missing = models.DateTimeField('Дата исчезновения', blank=True)

    def favourites_is_checked(self):
        if self.favourites == 1:
            return "checked"
        else:
            return ""

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"