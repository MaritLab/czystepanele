from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.templatetags.static import static
import random

from .models import (
    Category,
    Project,
    ProjectImage,
    Client,
    BlogPost,
    BlogCategory
)

# ============================================================
# STRONA GŁÓWNA
# ============================================================

def index(request):
    hero_images = [
        'images/mycie-okien-mercedes.webp',
        'images/hero.jpg',
        'images/hero2.jpg',
        'images/kolce.jpg',
        'images/okna.jpg',
    ]
    hero_image_urls = [static(p) for p in hero_images]
    background_image_url = random.choice(hero_image_urls)

    random_projects = Project.objects.order_by('?')[:3]
    clients = Client.objects.all().order_by('-created')

    return render(request, 'index.html', {
        'background_image_url': background_image_url,
        'hero_image_urls': hero_image_urls,
        'random_projects': random_projects,
        'clients': clients,
    })


# ============================================================
# PODSTRONY STATYCZNE
# ============================================================

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

def odsniezanie(request):
    return render(request, 'odsniezanie.html')


# ============================================================
# REALIZACJE – LISTA
# ============================================================

def realizacje(request):
    categories = Category.objects.prefetch_related('projects__images')
    projects = Project.objects.select_related('category')

    return render(request, 'realizacje.html', {
        'categories': categories,
        'projects': projects,
    })


# ============================================================
# REALIZACJE – PODGLĄD (preview.html)
# ============================================================

def preview_page(request, project_id, slug):
    project = get_object_or_404(Project, id=project_id, slug=slug)
    return render(request, 'preview.html', {
        'project': project
    })


# ============================================================
# REALIZACJE – AJAX (jeśli używasz)
# ============================================================

def get_project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    return JsonResponse({
        'title': project.title,
        'description': project.description,
        'date': project.date.strftime('%Y-%m-%d'),
        'main_image': project.main_image.url if project.main_image else None,
        'images': [img.image.url for img in project.images.all()],
    })


# ============================================================
# BLOG – LISTA WPISÓW
# ============================================================

def blog(request):
    posts = BlogPost.objects.select_related('category').prefetch_related('tags')
    categories = BlogCategory.objects.all()

    return render(request, 'blog.html', {
        'posts': posts,
        'categories': categories,
    })


# ============================================================
# BLOG – SZCZEGÓŁ WPISU
# ============================================================

def blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    latest_posts = BlogPost.objects.exclude(id=post.id)[:3]

    return render(request, 'blog_post.html', {
        'post': post,
        'latest_posts': latest_posts,
    })