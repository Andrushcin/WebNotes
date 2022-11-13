from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notes.models import Note
from django.views import View
from django.contrib.auth.models import User
from datetime import datetime

class MyNotes(View):
    def post(self, request):
        pass
    def get(self, request):
        try:
            order_by_param = request.GET['sort']
            if order_by_param not in ['date_update', '-date_update', 'date_create', '-date_create']:
                order_by_param = '-date_update'
        except:
            order_by_param = '-date_update'
    
        #notes = Note.objects.filter(user=request.user).order_by(order_by_param)
        user = User.objects.get(username=request.user)
        notes = user.note_set.all().order_by(order_by_param)#.values_list('name', 'id', named=True)

        missed_notes_ids = []
        current_notes_ids = []
        now = datetime.now()
        for n in notes:
            if n.date_missing < now:
                missed_notes_ids.append(n.id)
            else:
                current_notes_ids.append(n.id)
        
        missed_notes = notes
        missed_notes = missed_notes.filter(id__in=missed_notes_ids)
        notes = notes.filter(id__in=current_notes_ids)
        data = {
            'notes': notes,
            'missed_notes': missed_notes,
            }
        return render(request, 'notes/my_notes.html', data)

class CreateNote(View):
    def post(self, request):
        payload = request.POST.dict()
        if 'favourites' in payload.keys():
            favourites = payload['favourites']
        else:
            favourites = False
        
        user = User.objects.get(username=request.user)
        user.note_set.create(name=payload['name'], text=payload['text'], favourites=favourites, date_missing=payload['date_missing'])
        return HttpResponseRedirect('/notes/')
    
    def get(self, request):
        data = {
            "legend":"Новая заметка",
            "new": True,
        }
        return render(request, 'notes/change_note.html', data)


class ChangeNote(View):

    def post(self, request, pk):
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)

        payload = request.POST.dict()
        print(payload)
        note.name = payload['name']
        note.text = payload['text']

        if 'favourites' in payload.keys():
            note.favourites = payload['favourites']
        else:
            note.favourites = False
        
        if 'date_missing' in payload.keys():
            note.date_missing = payload['date_missing']

        note.save()

        return HttpResponseRedirect('/notes/')

    def get(self, request, pk):
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)
        data = {
            'note': note,
            'legend': "Редактирование заметки",
        }
        return render(request, 'notes/change_note.html', data)

class DeleteNote(View):

    def post(self, request, pk):
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)
        note.delete()
        return HttpResponseRedirect('/notes/')

class ChangeFavourites(View):
    def post(self, request, pk):
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)

        if note.favourites == False:
            note.favourites = True
        else:
            note.favourites = False
        note.save()

        return HttpResponseRedirect('/notes/')
