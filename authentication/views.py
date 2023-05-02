from django.shortcuts import render
from authentication.forms import *

def login(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        pass
    context = {'login_form': LoginForm()}
    return render(request, 'login.html', context)


def register(request):
    context = {
        'atlet_form': RegisterAtletForm(),
        'pelatih_form': RegisterPelatihForm(),
        'umpire_form': RegisterUmpireForm(),
    }
    return render(request, 'register.html', context)
