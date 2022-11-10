from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Note
from django.views import View

class MyNotes(View):

    def get(self, request):
        try:
            order_by_param = request.GET['sort']
            if order_by_param not in ['date_update', '-date_update']:
                order_by_param = '-date_update'
        except:
            order_by_param = '-date_update'
    
        notes = Note.objects.filter(user=request.user).order_by(order_by_param)
        data = {
            'notes': notes,
            }
        return render(request, 'notes/my_notes.html', data)

class CreateNote(View):
    def post(self, request):
        payload = request.POST.dict()
        if 'favourites' in payload.keys():
            favourites = payload['favourites']
        else:
            favourites = False

        Note.objects.create(user=request.user, name=payload['name'], text=payload['text'], favourites=favourites)
        return HttpResponseRedirect('/notes/')
    
    def get(self, request):
        return render(request, 'notes/change_note.html')


class ChangeNote(View):

    def post(self, request, pk):
        note = Note.objects.filter(user=request.user, id = pk)[0]

        payload = request.POST.dict()
        print(payload)
        note.name = payload['name']
        note.text = payload['text']
        if 'favourites' in payload.keys():
            note.favourites = payload['favourites']
        else:
            note.favourites = False
        note.save()

        return HttpResponseRedirect('/notes/')

    def get(self, request, pk):
        note = Note.objects.filter(user=request.user, id = pk)[0]

        return render(request, 'notes/change_note.html', {'note': note})

class DeleteNote(View):

    def post(self, request, pk):
        note = Note.objects.filter(user=request.user, id = pk)[0]
        note.delete()
        return HttpResponseRedirect('/notes/')

class ChangeFavourites(View):
    def post(self, request, pk):
        note = Note.objects.filter(user=request.user, id = pk)[0]

        if note.favourites == False:
            note.favourites = True
        else:
            note.favourites = False
        note.save()

        return HttpResponseRedirect('/notes/')
