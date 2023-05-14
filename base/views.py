from django.shortcuts import render, redirect

def main(request):
    if "id" in request.session:
        return redirect('dashboard:main')
    return render(request, 'index.html')

