from django.urls import path
from .views import RegisterView, register

urlpatterns = [
    #path('register', RegisterView.as_view()),
    path('register', register),
]