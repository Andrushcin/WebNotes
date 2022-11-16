from notes.models import Note
from django.contrib.auth.models import User

def check_payload_and_create_note(request):
    payload = request.POST.dict()
    user = User.objects.get(username=request.user)
    note = Note()

    if 'name' in payload.keys():
        note.name = payload['name']

    if 'text' in payload.keys():   
        note.text = payload['text']

    if 'favourites' in payload.keys() and isinstance(payload['favourites'], bool):
        note.favourites = payload['favourites']
    
    if 'date_missing' in payload.keys():
        note.date_to_trash = payload['date_missing']
    
    note.save()
    note = user.note_set.add(note)