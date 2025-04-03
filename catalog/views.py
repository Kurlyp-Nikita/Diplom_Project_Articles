from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Q
from catalog.forms import *
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@cache_page(60 * 15)  # Кеширование на 15 минут
def index(req):
    # Получаем последние статьи для отображения на главной странице
    latest_articles = Article.objects.all().order_by('-created_at')[:6]
    popular_articles = Article.objects.all().order_by('-views')[:3]
    
    data = {
        'latest_articles': latest_articles,
        'popular_articles': popular_articles,
    }
    return render(req, 'index.html', data)


class ArticleListView(ListView):
    model = Article
    template_name = 'catalog/article_list.html'
    paginate_by = 6
    context_object_name = 'articles'
    
    @method_decorator(cache_page(60 * 5))  # Кеширование на 5 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        topic_id = self.request.GET.get('topic')
        query = self.request.GET.get('query')
        
        if topic_id:
            queryset = queryset.filter(topic__name=topic_id)
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) |
                Q(text__icontains=query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET or None)
        context['topic_filter'] = self.request.GET.get('topic', '')
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'catalog/article_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        
        # Увеличиваем счетчик просмотров
        article.views += 1
        article.save()
        
        # Проверяем, поставил ли текущий пользователь лайк
        user_liked = False
        if self.request.user.is_authenticated:
            user_liked = article.likes.filter(user=self.request.user).exists()
        
        # Получаем оценку пользователя, если она есть
        user_rating = None
        if self.request.user.is_authenticated:
            rating = article.ratings.filter(user=self.request.user).first()
            if rating:
                user_rating = rating.value
        
        # Получаем данные для диаграммы рейтингов
        ratings_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        if article.ratings.exists():
            for rating in article.ratings.all():
                ratings_distribution[rating.value] += 1
        
        # Формируем форму комментария
        comment_form = CommentForm()
        
        # Связанные статьи (того же автора или той же категории)
        related_articles = Article.objects.filter(
            Q(author=article.author) | Q(topic=article.topic)
        ).exclude(id=article.id).distinct()[:3]
        
        context.update({
            'user_liked': user_liked,
            'comment_form': comment_form,
            'related_articles': related_articles,
            'user_rating': user_rating,
            'ratings_distribution': ratings_distribution,
            'avg_rating': article.get_average_rating(),
            'rating_count': article.get_rating_count(),
        })
        
        return context


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    
    return render(request, 'catalog/add_article.html', {'form': form})


@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    # Проверка, является ли пользователь автором статьи
    if article.author != request.user:
        return HttpResponseForbidden("Вы не имеете права редактировать эту статью")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'catalog/edit_article.html', {'form': form, 'article': article})


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    # Проверка, является ли пользователь автором статьи
    if article.author != request.user:
        return HttpResponseForbidden("Вы не имеете права удалить эту статью")
    
    if request.method == 'POST':
        article.delete()
        return redirect('articles_list')
    
    return render(request, 'catalog/delete_article_confirm.html', {'article': article})


@login_required
@require_POST
def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()
    
    return redirect('article_detail', pk=article.pk)


@login_required
@require_POST
def toggle_like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    user = request.user
    
    # Проверяем, существует ли уже лайк
    like_exists = Like.objects.filter(article=article, user=user).exists()
    
    if like_exists:
        # Если лайк существует, удаляем его
        Like.objects.filter(article=article, user=user).delete()
        liked = False
    else:
        # Если лайка нет, создаем новый
        Like.objects.create(article=article, user=user)
        liked = True
    
    # Возвращаем количество лайков и статус лайка пользователя
    likes_count = Like.objects.filter(article=article).count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'likes_count': likes_count,
            'liked': liked
        })
    else:
        return redirect('article_detail', pk=article.pk)


def reg(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            # Получение данных из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            # Создание нового пользователя
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()

            # Аутентификация пользователя
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')
    else:
        form = SignUp()

    context = {'form': form}
    return render(request, 'registration/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile_user(request):
    user = request.user
    articles = Article.objects.filter(author=user).order_by('-created_at')
    
    # Статистика пользователя
    total_articles = articles.count()
    total_likes = Like.objects.filter(article__author=user).count()
    total_comments = Comment.objects.filter(article__author=user).count()
    total_views = sum(article.views for article in articles)
    
    data = {
        'user': user,
        'articles': articles,
        'total_articles': total_articles,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_views': total_views,
    }
    
    return render(request, 'registration/profile_user.html', data)


def search_articles(request):
    form = SearchForm(request.GET)
    articles = Article.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        topic = form.cleaned_data.get('topic')
        
        if query:
            articles = articles.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) |
                Q(text__icontains=query)
            )
        
        if topic:
            articles = articles.filter(topic=topic)
    
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalog/search_results.html', {
        'form': form,
        'page_obj': page_obj,
        'query': request.GET.get('query', ''),
    })


@cache_page(60 * 5)  # Кеширование на 5 минут
def articles_by_topic(request, topic_name):
    """Функция для отображения статей по категориям с ЧПУ-ссылками"""
    articles = Article.objects.filter(topic__name=topic_name)
    
    # Пагинация
    paginator = Paginator(articles, 6)  # По 6 статей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'articles': page_obj,
        'topic_name': topic_name,
        'page_obj': page_obj,
    }
    
    return render(request, 'catalog/articles_by_topic.html', context)


@login_required
def rate_article(request, pk):
    """Функция для оценки статьи"""
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        
        if 1 <= rating_value <= 5:  # Проверяем, что оценка в пределах от 1 до 5
            # Проверяем, голосовал ли пользователь ранее
            rating, created = Rating.objects.get_or_create(
                article=article,
                user=request.user,
                defaults={'value': rating_value}
            )
            
            # Если пользователь уже голосовал, обновляем значение
            if not created:
                rating.value = rating_value
                rating.save()
            
            # Получаем новое среднее значение
            avg_rating = article.get_average_rating()
            rating_count = article.get_rating_count()
            
            # Если это AJAX запрос, возвращаем JSON с новыми данными
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'avg_rating': avg_rating,
                    'rating_count': rating_count,
                    'success': True
                })
    
    # Перенаправляем на страницу статьи
    return redirect('article_detail', pk=pk)

