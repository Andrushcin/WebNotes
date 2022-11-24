from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from notes.models import Note
from django.views import View
from django.urls import reverse
from notes.methods import *

class MyNotes(View):
    @message_for_anonymous
    def get(self, request):
        available_sort_params = ['date_update', 'date_create', 'date_to_trash']

        sort_param = get_sort_param(request, available_sort_params)
        select_param = get_select_param(sort_param, available_sort_params)
        instance = get_instance(request)
        notes = get_notes_for_user(instance, sort_param)

        current_notes = notes
        current_notes_ids = [n.id for n in current_notes if not n.in_trash()]
        current_notes = notes.filter(id__in=current_notes_ids).values_list('name', 'id', 'favourites', named=True)

        data = {
            'notes': current_notes,
            'select_param':select_param,
            }
        return render(request, 'notes/my_notes.html', data)

class TrashCanView(View):
    @message_for_anonymous
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
    
    @message_for_anonymous
    def get(self, request):
        data = {
            "legend":"Новая заметка",
            "new": True,
        }
        return render(request, 'notes/change_note.html', data)

class ChangeNote(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = get_object_or_404(instance.note_set, id=pk)

        payload = request.POST.dict()
        add_data_from_payload(note, payload)
        return HttpResponseRedirect('/notes/')

    @message_for_anonymous
    def get(self, request, pk):
        instance = get_instance(request)
        note = get_object_or_404(instance.note_set, id=pk)

        data = {
            'note': note,
            'legend': "Редактирование заметки",
        }
        return render(request, 'notes/change_note.html', data)

class DeleteNote(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = get_object_or_404(instance.note_set, id=pk)

        note.delete()
        return HttpResponseRedirect(reverse('notes:index'))

class ChangeFavourites(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = get_object_or_404(instance.note_set, id=pk)

        note.change_favourites()
        note.save()
        return HttpResponseRedirect('/notes/')

class RecoverNote(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = get_object_or_404(instance.note_set, id=pk)

        note.out_of_trash()
        note.save()
        return HttpResponseRedirect('/notes/trash')

class ToTrashCan(View):
    def post(self, request, pk):
        instance = get_instance(request)
        note = get_object_or_404(instance.note_set, id=pk)

        note.to_trash()
        note.save()
        return HttpResponseRedirect('/notes/')
