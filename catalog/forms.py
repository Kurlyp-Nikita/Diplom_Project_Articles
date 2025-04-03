from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['topic', 'title', 'summary', 'text', 'info', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 15, 'class': 'article-text'}),
            'summary': forms.Textarea(attrs={'rows': 3, 'class': 'article-summary'}),
            'title': forms.TextInput(attrs={'class': 'article-title'}),
            'topic': forms.Select(attrs={'class': 'article-topic'}),
            'info': forms.URLInput(attrs={'class': 'article-info'}),
            'image': forms.URLInput(attrs={'class': 'article-image'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'comment-text', 'placeholder': 'Оставьте ваш комментарий...'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск', 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Введите слово для поиска...', 'class': 'search-input'})
    )
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        required=False,
        empty_label="Все категории",
        widget=forms.Select(attrs={'class': 'topic-filter'})
    )


class SignUp(UserCreationForm):
    username = forms.CharField(label='логин',
                               help_text='',
                               widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-input'}))
    password1 = forms.CharField(label='пароль',
                                help_text='', widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-input'}
        )
                                )
    password2 = forms.CharField(label='подтверждение',
                                help_text='', widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-input'}
        )
                                )
    email = forms.EmailField(label='почта',
                             widget=forms.TextInput(attrs={'placeholder': 'qwe@mail.ru', 'class': 'form-input'})
                             )
    first_name = forms.CharField(label='имя', max_length=20, required=False, 
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='фамилия', max_length=20, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

