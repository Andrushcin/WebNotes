from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from info.models import InfoPart
from notes.models import Note
import requests
from random import randint, random
from datetime import timedelta

class AddView(View):

    def get(self, request):
        for i in range(20):
            pr = randint(1, 10)
            text = requests.get(f"https://baconipsum.com/api/?type=meat-and-filler&paras={pr}&format=text").text

            name = requests.get(f"https://baconipsum.com/api/?type=all-meat&sentences=1").text[2:randint(10, 98)]

            if randint(1, 100)%2 == 1:
                fav = True
            else:
                fav = False

            Note.objects.create(user='admin',
                name=name,
                text=text,
                favourites=fav,
                life_time=timedelta(days=randint(1, 100))
                )

        return HttpResponse('data was received')
