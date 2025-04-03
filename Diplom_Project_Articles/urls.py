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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    
    # Статьи
    path('articles/', views.ArticleListView.as_view(), name='articles_list'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/add/', views.add_article, name='add_article'),
    path('articles/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('articles/category/<str:topic_name>/', views.articles_by_topic, name='articles_by_topic'),
    
    # Комментарии и лайки
    path('articles/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('articles/<int:pk>/toggle_like/', views.toggle_like, name='toggle_like'),
    path('articles/<int:pk>/rate/', views.rate_article, name='rate_article'),
    
    # Поиск
    path('search/', views.search_articles, name='search_articles'),
    
    # Аутентификация
    path('registration/', views.reg, name='reg'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_user, name='profile'),
]

# Добавляем обработку статических файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
