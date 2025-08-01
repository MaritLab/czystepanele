from django.shortcuts import render
from .models import Category
from django.http import JsonResponse, Http404
from .models import Project
import random

def index(request):
    hero_images = [
        'images/mycie-okien-mercedes.webp',
        'images/hero.jpg',
        'images/hero2.jpg',
        'images/kolce.jpg',
        'images/okna.jpg',
    ]
    selected_image = random.choice(hero_images)
    return render(request, 'index.html', {
        'background_image' : selected_image
    })
    

def kontakt(request):
    return render(request, 'kontakt.html')

def mycie_paneli(request):
    return render(request, 'mycie-paneli.html')

def mycie_okien(request):
    return render(request, 'mycie-okien.html')

def koszenie_trawnikow(request):
    return render(request, 'koszenie-trawnikow.html')

def zabezpieczenia_przed_ptakami(request):
    return render(request, 'zabezpieczenia-przed-ptakami.html')

def uslugi_wysokosciowe(request):
    return render(request, 'uslugi-wysokosciowe.html')

def realizacje(request):
    return render(request, 'realizacje.html')

def blog(request):
    return render(request, 'blog.html')

def gallery_view(request):
    categories = Category.objects.prefetch_related('projects__images')
    return render(request, 'realizacje.html', {'categories': categories})

def get_project_details(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404("Projekt nie istnieje.")

    data = {
        'title': project.title,
        'description': project.description,
        'date': project.date.strftime("%Y-%m-%d"),
        'images': [img.image.url for img in project.images.all()]
    }
    return JsonResponse(data)

def preview_page(request, project_id, slug):
    return render(request, 'preview.html')

