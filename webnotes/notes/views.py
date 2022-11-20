from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notes.models import Note
from django.views import View
from django.contrib.auth.models import User, AnonymousUser
from datetime import datetime
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user
from django.contrib.sessions.backends.db import SessionStore

def add_data_from_payload(note, payload):
    if 'name' in payload.keys():
        note.name = payload['name']

    if 'text' in payload.keys():   
        note.text = payload['text']

    if 'favourites' in payload.keys():
        note.favourites = bool(payload['favourites'])
    
    if 'date_missing' in payload.keys():
        if payload['date_missing'] != "":
            note.date_to_trash = payload['date_missing']
    
    note.save()
    return note
    
class MyNotes(View):
    def post(self, request):
        pass
    def get(self, request):
        available_sort_params = ['date_update', 'date_create', 'date_to_trash']
        params = request.GET
        sort_reverse = False
        order_by_param = 'date_update'

        if 'sort' in params.keys():
            if params['sort'] in available_sort_params:
                order_by_param = params['sort']

        if 'reverse' in params.keys():
            if params['reverse'] == "true":
                sort_reverse = True

        select_param = {}
        for var in available_sort_params:
            if var == order_by_param:
                select_param[var] = "selected"
            else:
                select_param[var] = ""

        if not sort_reverse:
            order_by_param = "-" + order_by_param

        if isinstance(get_user(request), AnonymousUser):
            print(request.session.exists(request.session.session_key))
            if request.session.session_key == None:
                request.session.cycle_key()
            
            session = Session.objects.filter(session_key = request.session.session_key)[0]
            notes = session.note_set.all().order_by(order_by_param)
        else:
            user = User.objects.get(username=request.user)
            notes = user.note_set.all().order_by(order_by_param)

        current_notes = notes
        current_notes_ids = [n.id for n in current_notes if not n.in_trash()]
        current_notes = notes.filter(id__in=current_notes_ids).values_list('name', 'id', 'favourites', named=True)
        
        data = {
            'notes': current_notes,
            'select_param':select_param,
            }
        return render(request, 'notes/my_notes.html', data)

class CreateNote(View):
    def post(self, request):
        payload = request.POST.dict()
        note = Note()

        if isinstance(get_user(request), AnonymousUser): 
            if request.session.session_key == None:
                request.session.cycle_key()
                   
            session = Session.objects.filter(session_key = request.session.session_key)[0]
            session.note_set.add(add_data_from_payload(note, payload))
        else:
            user = User.objects.get(username=request.user)
            user.note_set.add(add_data_from_payload(note, payload))
        
        return HttpResponseRedirect('/notes/')
    
    def get(self, request):
        data = {
            "legend":"Новая заметка",
            "new": True,
        }
        return render(request, 'notes/change_note.html', data)


class ChangeNote(View):
    def post(self, request, pk):
        payload = request.POST.dict()
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)

        add_data_from_payload(note, payload)
        return HttpResponseRedirect('/notes/')

    def get(self, request, pk):
        user = User.objects.get(username=request.user)
        try:
            note = user.note_set.get(id=pk)
        except Exception as e:
            return HttpResponseNotFound()
        
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
        return HttpResponseRedirect(reverse('notes:trash'))

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

        return HttpResponseRedirect('/notes/trash')

class ToTrashCan(View):
    def post(self, request, pk):
        user = User.objects.get(username=request.user)
        note = user.note_set.get(id=pk)

        note.to_trash()
        note.save()

        return HttpResponseRedirect('/notes/')
