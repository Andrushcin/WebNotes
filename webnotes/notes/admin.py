from django.contrib import admin
from .models import Note
admin.site.register(Note)
admin.site.site_header = 'Webnotes - администрирование'
