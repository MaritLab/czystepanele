from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def kontakt(request):
    return render(request, 'kontakt.html')

def mycie_paneli(request):
    return render(request, 'mycie-paneli.html')

def mycie_okien(request):
    return render(request, 'mycie-okien.html')

def koszenie_trawnikow(request):
    return render(request, 'koszenie-trawnikow.html')

def zabezpieczenia_przeciwko_ptakom(request):
    return render(request, 'zabezpieczenia-przeciwko-ptakom.html')

def uslugi_wysokosciowe(request):
    return render(request, 'uslugi-wysokosciowe.html')

def realizacje(request):
    return render(request, 'realizacje.html')

def blog(request):
    return render(request, 'blog.html')
