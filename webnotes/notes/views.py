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

def get_instance(request):
    if isinstance(get_user(request), AnonymousUser):
        if request.session.session_key == None:
            request.session.cycle_key()
        
        session = Session.objects.filter(session_key = request.session.session_key)[0]
        return session
    else:
        user = User.objects.get(username=request.user)
        return user

def get_notes_for_user(instance, sort_params):
    order_by_param = sort_params["order_by"]
    if not sort_params["reverse"]:
        order_by_param = "-" + sort_params["order_by"]

    notes = instance.note_set.all().order_by(order_by_param)
    
    return notes

def get_sort_param(request, available_sort_params):
    params = request.GET
    reverse = False
    order_by = 'date_update'

    if 'sort' in params.keys():
        if params['sort'] in available_sort_params:
            order_by = params['sort']

    if 'reverse' in params.keys():
        if params['reverse'] == "true":
            reverse = True
    
    return {"order_by": order_by,
            "reverse": reverse}

def get_select_param(sort_param, available_sort_params):
    select_param = {}
    for var in available_sort_params:
        if var == sort_param["order_by"]:
            select_param[var] = "selected"
        else:
            select_param[var] = ""
    return select_param
    
class MyNotes(View):
    def get(self, request):
        available_sort_params = ['date_update', 'date_create', 'date_to_trash']

        sort_param = get_sort_param(request, available_sort_params)
        select_param = get_select_param(sort_param, available_sort_params)
        instance = get_instance(request)
        print(request.user)
        print(instance)
        notes = get_notes_for_user(instance, sort_param)

        current_notes = notes
        current_notes_ids = [n.id for n in current_notes if not n.in_trash()]
        current_notes = notes.filter(id__in=current_notes_ids).values_list('name', 'id', 'favourites', named=True)
        
        message = ""
        if isinstance(instance, AnonymousUser):
            message = "Внимание! Вы не авторизованы в системе, поэтому при завершении сеанса вы потеряете доступ к своим заметкам."

        data = {
            'notes': current_notes,
            'select_param':select_param,
            'message':message,
            }
        return render(request, 'notes/my_notes.html', data)

class TrashCanView(View):
    def get(self, request):
        available_sort_params = ['date_update', 'date_create', 'date_to_trash']

        sort_param = get_sort_param(request, available_sort_params)
        select_param = get_select_param(sort_param, available_sort_params)
        instance = get_instance(request)
        notes = get_notes_for_user(instance, sort_param)

        missed_notes = notes
        missed_notes_ids = [n.id for n in missed_notes if n.in_trash()]
        missed_notes = notes.filter(id__in=missed_notes_ids).values_list('name', 'id', 'favourites', named=True)

        data = {
            'notes': missed_notes,
            'select_param':select_param,
            'trash': True,
            }
        return render(request, 'notes/my_notes.html', data)

class CreateNote(View):
    def post(self, request):
        payload = request.POST.dict()
        note = Note()

        instance = get_instance(request)
        instance.note_set.add(add_data_from_payload(note, payload))
        
        return HttpResponseRedirect('/notes/')
    
    def get(self, request):
        data = {
            "legend":"Новая заметка",
            "new": True,
        }
        return render(request, 'notes/change_note.html', data)

class ChangeNote(View):
    
    def post(self, request, pk):
        instance = get_instance(request)
        note = instance.note_set.get(id=pk)

        payload = request.POST.dict()
        add_data_from_payload(note, payload)
        return HttpResponseRedirect('/notes/')

    def get(self, request, pk):
        instance = get_instance(request)
        try:
            note = instance.note_set.get(id=pk)
        except Exception as e:
            return HttpResponseNotFound()
        
        data = {
            'note': note,
            'legend': "Редактирование заметки",
        }
        return render(request, 'notes/change_note.html', data)

class DeleteNote(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = instance.note_set.get(id=pk)
        note.delete()
        return HttpResponseRedirect(reverse('notes:trash'))

class ChangeFavourites(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = instance.note_set.get(id=pk)
        note.change_favourites()
        note.save()
        return HttpResponseRedirect('/notes/')

class RecoverNote(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = instance.note_set.get(id=pk)

        note.out_of_trash()
        note.save()

        return HttpResponseRedirect('/notes/trash')

class ToTrashCan(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = instance.note_set.get(id=pk)

        note.to_trash()
        note.save()

        return HttpResponseRedirect('/notes/')
