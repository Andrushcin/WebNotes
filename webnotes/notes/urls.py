from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "notes"
urlpatterns = [
    path('', login_required(MyNotes.as_view()), name='index'),
    path('new', login_required(CreateNote.as_view()), name="new"),
    path('trash', login_required(TrashCanView.as_view()), name="trash"),
    path('<int:pk>', login_required(ChangeNote.as_view()), name="note"),
    path('delete/<int:pk>', login_required(DeleteNote.as_view()), name="delete"),
    path('change_favourites/<int:pk>', login_required(ChangeFavourites.as_view()), name="change_favourites"),
    path('to_trash/<int:pk>', login_required(ToTrashCan.as_view()), name="to_trash"),
    path('recover/<int:pk>', login_required(RecoverNote.as_view()), name="recover"),
]
