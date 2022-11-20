from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Название заметки', max_length=100, blank=True)
    text = models.TextField('Текст заметки', max_length=1000, blank=True)
    favourites = models.BooleanField('Добавить в избранное', default=False, blank=True)
    date_update = models.DateTimeField('Дата последнего изменения', auto_now=True)
    date_create = models.DateTimeField('Дата создания', auto_now_add=True) 
    date_to_trash = models.DateTimeField('Дата удаления', blank=True, null=True)

    def favourites_is_checked(self):
        if self.favourites == 1:
            return "checked"
        else:
            return ""

    def date_missing_string(self):
        if self.date_to_trash is not None:
            return self.date_to_trash.strftime("%Y-%m-%dT%H:%M")
        else:
            return ""
    
    def to_trash(self):
        self.date_to_trash = datetime.now()
    
    def out_of_trash(self):
        self.date_to_trash = None
    
    def in_trash(self):
        if self.date_to_trash is not None:
            if self.date_to_trash < datetime.now():
                return True
        else:
            return False

    def change_favourites(self):
        if self.favourites:
            self.favourites = False
        else:
            self.favourites = True
    
    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
