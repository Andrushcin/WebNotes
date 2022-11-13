from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название заметки', max_length=100, blank=True)
    text = models.TextField('Текст заметки', max_length=1000, blank=True)
    favourites = models.BooleanField('Добавить в избранное', default=False, blank=True)
    date_update = models.DateTimeField('Дата последнего изменения', auto_now=True)
    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    date_missing = models.DateTimeField('Дата исчезновения', blank=True, null=True)

    def favourites_is_checked(self):
        if self.favourites == 1:
            return "checked"
        else:
            return ""

    def date_missing_string(self):
        return self.date_missing.strftime("%Y-%m-%dT%H:%M")

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
