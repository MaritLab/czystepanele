from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('mycie-paneli/', views.mycie_paneli, name='mycie-paneli'),
    path('mycie-okien/', views.mycie_okien, name='mycie-okien'),
    path('koszenie-trawnikow/', views.koszenie_trawnikow, name='koszenie-trawnikow'),
    path('zabezpieczenia-przeciwko-ptakom/', views.zabezpieczenia_przeciwko_ptakom, name='zabezpieczenia-przeciwko-ptakom'),
    path('uslugi-wysokosciowe/', views.uslugi_wysokosciowe, name='uslugi-wysokosciowe'),
    path('realizacje/', views.realizacje, name='realizacje'),
    path('blog/', views.blog, name='blog'),
]
