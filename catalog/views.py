from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView  # функция генерации чего-то
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, HttpResponse
from catalog.forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib.auth.hashers import make_password


def index(req):
    data = {}
    return render(req, 'index.html', data)


class ArticleSienceListView(ListView):
    model = Sience
    paginate_by = 3


class ArticleSienceDetailView(DetailView):
    model = Sience


class ArticleSportListView(ListView):
    model = Sport
    paginate_by = 3


class ArticleSportDetailView(DetailView):
    model = Sport


class ArticleArtListView(ListView):
    model = Art
    paginate_by = 3


class ArticleArtDetailView(DetailView):
    model = Art


# Функции добавления статей
def addarticles(req):
    user = req.user  # используйте req.user для доступа к аутентифицированному пользователю
    if req.POST:
        k1 = req.POST.get('topic')
        k2 = req.POST.get('title')
        k3 = req.POST.get('summary')
        k4 = req.POST.get('text')
        k5 = req.POST.get('data')
        k6 = req.POST.get('info')
        k7 = req.user.username
        k8 = req.POST.get('image')

        print(k1, k2, k3, k4, k5, k6, k7, k8)

        if k1 == '1':
            science_form = SienceForm(req.POST)
            if science_form.is_valid():
                science = science_form.save(commit=False)
                science.topic_id = k1
                science.author = user
                science.save()
                return redirect('allsience')

        elif k1 == '2':
            sport_form = SportForm(req.POST)
            if sport_form.is_valid():
                sport = sport_form.save(commit=False)
                sport.topic_id = k1
                sport.author = user
                sport.save()
                return redirect('allsport')

        elif k1 == '3':
            art_form = ArtForm(req.POST)
            if art_form.is_valid():
                art = art_form.save(commit=False)
                art.topic_id = k1
                art.author = user
                art.save()
                return redirect('allart')

    else:
        science_form = SienceForm(initial={'author': user})  # инициализируйте форму со значением автора
        sport_form = SportForm(initial={'author': user})
        art_form = ArtForm(initial={'author': user})
        data = {'science_form': science_form, 'sport_form': sport_form, 'art_form': art_form}
        return render(req, 'catalog/add_articles.html', data)


 # Функции удаления статей
def delete_sience_articles(req, id):
    one_sience = Sience.objects.get(id=id)
    one_sience.delete()
    return redirect('allsience')


def delete_sport_articles(req, id):
    one_sport = Sport.objects.get(id=id)
    one_sport.delete()
    return redirect('allsport')


def delete_art_articles(req, id):
    one_art = Art.objects.get(id=id)
    one_art.delete()
    return redirect('allart')


# Функции изменения статей
def edit_sience(req, id):
    onesience = Sience.objects.get(id=id)

    if onesience.author != req.user:
        return HttpResponseForbidden("Вы не имеете права изменять эту статью")

    forma = SienceForm(instance=onesience)

    if req.POST:
        form = SienceForm(req.POST, instance=onesience)
        if form.is_valid():
            form.save()
            return redirect('allsience')

    data = {'forma': forma}
    return render(req, 'catalog/edit_sience.html', data)


def edit_sport(req, id):
    onesport = Sport.objects.get(id=id)

    if onesport.author != req.user:
        return HttpResponseForbidden("Вы не имеете права изменять эту статью")

    forma = SportForm(instance=onesport)

    if req.POST:
        form = SportForm(req.POST, instance=onesport)
        if form.is_valid():
            form.save()
            return redirect('allsport')

    data = {'forma': forma}
    return render(req, 'catalog/edit_sport.html', data)


def edit_art(req, id):
    oneart = Art.objects.get(id=id)

    if oneart.author != req.user:
        return HttpResponseForbidden("Вы не имеете права изменять эту статью")

    forma = ArtForm(instance=oneart)

    if req.POST:
        form = ArtForm(req.POST, instance=oneart)
        if form.is_valid():
            form.save()
            return redirect('allart')

    data = {'forma': forma}
    return render(req, 'catalog/edit_art.html', data)


def reg(request):
    if request.POST:  # Проверка на POST запрос
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
                # Перенаправление на главную страницу или другой URL
                return redirect('login')
    else:
        form = SignUp()

    context = {'form': form}
    return render(request, 'registration/registration.html', context)


def user_login(request):
    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправление на главную страницу после входа
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def profile_user(req):
    if req.user.is_authenticated:
        sience = Sience.objects.filter(author=req.user)
        sport = Sport.objects.filter(author=req.user)
        art = Art.objects.filter(author=req.user)
        forma_sience = SienceForm()
        forma_sport = SportForm()
        forma_art = ArtForm()
        user = req.user

        if req.POST:
            if 'sience_form' in req.POST:
                forma_sience = SienceForm(req.POST)
                if forma_sience.is_valid():
                    new_sience = forma_sience.save(commit=False)
                    new_sience.author = req.user
                    new_sience.save()

            elif 'sport_form' in req.POST:
                forma_sport = SportForm(req.POST)
                if forma_sport.is_valid():
                    new_sport = forma_sport.save(commit=False)
                    new_sport.author = req.user
                    new_sport.save()

            elif 'art_form' in req.POST:
                forma_art = ArtForm(req.POST)
                if forma_art.is_valid():
                    new_art = forma_art.save(commit=False)
                    new_art.author = req.user
                    new_art.save()

        data = {
            'database_sience': sience,
            'forma_sience': forma_sience,
            'database_sport': sport,
            'forma_sport': forma_sport,
            'database_art': art,
            'forma_art': forma_art
        }
        return render(req, 'registration/profile_user.html', data)
    else:
        return HttpResponse('<h1>Сначала авторизуйтесь</h1>')

