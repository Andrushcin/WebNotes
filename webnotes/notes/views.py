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
    
        user = User.objects.get(username=request.user)
        notes = user.note_set.all().order_by(order_by_param)

        current_notes = notes
        current_notes_ids = [n.id for n in current_notes if not n.in_trash()]
        current_notes = notes.filter(id__in=current_notes_ids).values_list('name', 'id', 'favourites', named=True)

        data = {
            'notes': current_notes,
            }
        return render(request, 'notes/my_notes.html', data)

class CreateNote(View):
    def post(self, request):
        payload = request.POST.dict()
        if 'favourites' in payload.keys() and isinstance(payload['date_missing'], datetime):
            favourites = payload['favourites']
        
        user = User.objects.get(username=request.user)
        user.note_set.create(name=payload['name'], text=payload['text'], favourites=favourites, date_to_trash=payload['date_missing'])
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

        if 'name' in payload.keys():
            note.name = payload['name']

        if 'text' in payload.keys():   
            note.text = payload['text']

        if 'favourites' in payload.keys() and isinstance(payload['favourites'], bool):
            note.favourites = payload['favourites']
        
        if 'date_missing' in payload.keys() and isinstance(payload['date_missing'], datetime):
                note.date_to_trash = payload['date_missing']

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
        note.to_trash()
        return HttpResponseRedirect('/notes/')

class ChangeFavourites(View):
    def post(self, request, pk):
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)
        note.change_favourites()
        note.save()
        return HttpResponseRedirect('/notes/')

class TrashCanView(View):
    def get(self, request):
        try:
            order_by_param = request.GET['sort']
            if order_by_param not in ['date_update', '-date_update', 'date_create', '-date_create']:
                order_by_param = '-date_update'
        except:
            order_by_param = '-date_to_trash'
    
        user = User.objects.get(username=request.user)
        notes = user.note_set.all().order_by(order_by_param)

        missed_notes = notes
        missed_notes_ids = [n.id for n in missed_notes if n.in_trash()]
        missed_notes = notes.filter(id__in=missed_notes_ids).values_list('name', 'id', 'favourites', named=True)

        data = {
            'notes': missed_notes,
            'trash': True,
            }
        return render(request, 'notes/my_notes.html', data)

class RecoverNote(View):
    def post(self, request, pk):
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)

        note.out_of_trash()
        note.save()

        return HttpResponseRedirect('/notes/')

class ToTrashCan(View):
    def post(self, request, pk):
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)

        note.to_trash()
        note.save()

        return HttpResponseRedirect('/notes/')