from django.urls import path
from .views import *

app_name = "notes"
urlpatterns = [
    path('', InfoView.as_view(), name='index'),
]
