"""
URL configuration for Diplom_Project_Articles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('addarticles/', views.addarticles, name='addarticles'),
    path('edit_sience/<int:id>/', views.edit_sience, name='edit_sience'),
    path('edit_sport/<int:id>/', views.edit_sport, name='edit_sport'),
    path('edit_art/<int:id>/', views.edit_art, name='edit_art'),

    path('delete_sience_articles/<int:id>/', views.delete_sience_articles, name='delete_sience'),
    path('delete_sport_articles/<int:id>/', views.delete_sport_articles, name='delete_sport'),
    path('delete_art_articles/<int:id>/', views.delete_art_articles, name='delete_art'),

    path('sience_articles/all/', views.ArticleSienceListView.as_view(), name='allsience'),
    path('info_sience_aerticles/<int:pk>/', views.ArticleSienceDetailView.as_view(), name='info_sience'),
    path('sport_articles/all/', views.ArticleSportListView.as_view(), name='allsport'),
    path('info_sport_aerticles/<int:pk>/', views.ArticleSportDetailView.as_view(), name='info_sport'),
    path('art_articles/all/', views.ArticleArtListView.as_view(), name='allart'),
    path('info_art_aerticles/<int:pk>/', views.ArticleArtDetailView.as_view(), name='info_art'),

    path('registration/', views.reg, name='reg'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_user, name='profile'),
]
