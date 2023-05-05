from django.shortcuts import render, redirect

def main(request):
    # temporary role authorization goes here
    request.session['email'] = 'john.smith@ristek.cs.ui.ac.id'
    request.session['is_atlet'] = False
    request.session['is_pelatih'] = False
    request.session['is_umpire'] = False
    if request.session['is_atlet'] or request.session['is_pelatih'] or request.session['is_umpire'] :
        return redirect('dashboard:main')
    return render(request, 'index.html')
