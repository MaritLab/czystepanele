from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('kontakt/', views.kontakt, name='kontakt'),
    path('mycie-paneli/', views.mycie_paneli, name='mycie-paneli'),
    path('mycie-okien/', views.mycie_okien, name='mycie-okien'),
    path('koszenie-trawnikow/', views.koszenie_trawnikow, name='koszenie-trawnikow'),
    path('zabezpieczenia-przed-ptakami/', views.zabezpieczenia_przed_ptakami, name='zabezpieczenia-przed-ptakami'),
    path('uslugi-wysokosciowe/', views.uslugi_wysokosciowe, name='uslugi-wysokosciowe'),
    path('odsniezanie/', views.odsniezanie, name='odsniezanie'),

    # REALIZACJE
    path('realizacje/', views.realizacje, name='realizacje'),
    path('realizacja/<int:project_id>-<slug:slug>/', views.preview_page, name='preview_slug'),
    path('get_project_details/<int:project_id>/', views.get_project_details, name='get_project_details'),

    # BLOG
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_post, name='blog_post'),
]