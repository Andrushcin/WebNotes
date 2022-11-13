from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from info.models import InfoPart
from notes.models import Note
import requests
from random import randint, random
from datetime import datetime
from django.contrib.auth.models import User

class AddView(View):

    def get(self, request):
        for i in range(50):
            pr = randint(1, 10)
            text = requests.get(f"https://baconipsum.com/api/?type=meat-and-filler&paras={pr}&format=text").text

            name = requests.get(f"https://baconipsum.com/api/?type=all-meat&sentences=1").text[2:randint(10, 98)]

            if randint(1, 100)%2 == 1:
                fav = True
            else:
                fav = False

            user = User.objects.get(username=request.user)
            try:
                user.note_set.create(
                    name=name,
                    text=text,
                    favourites=fav,
                    date_missing=datetime(year=2022, month=randint(11, 12), day=randint(14, 30), hour=randint(0, 23), minute=randint(0, 59))
                    )
            except Exception as e:
                print(e)

        return HttpResponse('data was received')
