from django.shortcuts import render

def main(request):
    # temporary role authorization goes here
    request.session['is_atlet'] = True
    request.session['is_pelatih'] = False
    request.session['is_umpire'] = False
    return render(request, 'index.html')
