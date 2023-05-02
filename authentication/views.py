from django.shortcuts import render
from authentication.forms import LoginForm

def login(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        pass
    context = {'login_form':LoginForm()}
    return render(request, 'login.html', context)

def register(request):
    return render(request, 'register.html')