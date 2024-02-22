from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Topic(models.Model):
    VIBOR = (('Наука', 'Наука'), ('Спорт', 'Спорт'), ('Искусство', 'Искусство'))
    name = models.CharField(max_length=100, choices=VIBOR, verbose_name='Тема статьи')

    def __str__(self):
        return self.name


class Sience(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000, verbose_name='Название статьи')
    summary = models.CharField(max_length=1000, verbose_name='кратко о статье', blank=True, null=True)
    text = models.TextField(max_length=10000000000000000, verbose_name='текст статьи', blank=True, null=True)
    data = models.DateField(verbose_name='Дата публикации статьи', blank=True, null=True)
    info = models.URLField(verbose_name='Источник(и)', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')  # поле author
    image = models.URLField(verbose_name='Фото', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('info_sience', args=[self.id])


class Sport(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000, verbose_name='Название статьи')
    summary = models.CharField(max_length=1000, verbose_name='кратко о статье', blank=True, null=True)
    text = models.TextField(max_length=10000000000000000, verbose_name='текст статьи', blank=True, null=True)
    data = models.DateField(verbose_name='Дата публикации статьи', blank=True, null=True)
    info = models.URLField(verbose_name='Источник(и)', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')  # поле author
    image = models.URLField(verbose_name='Фото', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('info_sport', args=[self.id])


class Art(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000, verbose_name='Название статьи')
    summary = models.CharField(max_length=1000, verbose_name='кратко о статье', blank=True, null=True)
    text = models.TextField(max_length=10000000000000000, verbose_name='текст статьи', blank=True, null=True)
    data = models.DateField(verbose_name='Дата публикации статьи', blank=True, null=True)
    info = models.URLField(verbose_name='Источник(и)', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')  # поле author
    image = models.URLField(verbose_name='Фото', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('info_art', args=[self.id])
