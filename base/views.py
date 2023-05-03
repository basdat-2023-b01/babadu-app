from django.shortcuts import render

def main(request):
    request.session['is_atlet'] = False
    request.session['is_pelatih'] = False
    request.session['is_umpire'] = True
    return render(request, 'index.html')
