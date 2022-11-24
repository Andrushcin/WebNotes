from django.shortcuts import render
from django.contrib import messages
from .forms import UserRegisterForm
from django.http import HttpResponseRedirect
from django.views import View

class RegisterView(View):
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return HttpResponseRedirect('/accounts/login')
    
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})
