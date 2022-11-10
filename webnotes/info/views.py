from django.shortcuts import render
from django.views.generic import ListView
from .models import InfoPart

class InfoView(ListView):
    template_name = 'info/info_page.html'
    model = InfoPart

