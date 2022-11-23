from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "notes"
urlpatterns = [
    path('', MyNotes.as_view(), name='index'),
    path('new', CreateNote.as_view(), name="new"),
    path('trash', TrashCanView.as_view(), name="trash"),
    path('<int:pk>', ChangeNote.as_view(), name="note"),
    path('delete/<int:pk>', DeleteNote.as_view(), name="delete"),
    path('change_favourites/<int:pk>', ChangeFavourites.as_view(), name="change_favourites"),
    path('to_trash/<int:pk>', ToTrashCan.as_view(), name="to_trash"),
    path('recover/<int:pk>', RecoverNote.as_view(), name="recover"),
]
