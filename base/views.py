from django.shortcuts import render, redirect
from django.db import connection
from base.helper.function import parse

def main(request):
    if "id" in request.session:
        return redirect('dashboard:main')
    return render(request, 'index.html')

