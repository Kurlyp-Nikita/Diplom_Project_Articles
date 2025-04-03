from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg


class Topic(models.Model):
    SCIENCE = 'Наука'
    SPORT = 'Спорт'
    ART = 'Искусство'
    
    VIBOR = (
        (SCIENCE, 'Наука'),
        (SPORT, 'Спорт'),
        (ART, 'Искусство')
    )
    name = models.CharField(max_length=100, choices=VIBOR, verbose_name='Тема статьи')

    def __str__(self):
        return self.name


class Article(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    title = models.CharField(max_length=1000, verbose_name='Название статьи')
    summary = models.CharField(max_length=1000, verbose_name='Кратко о статье', blank=True, null=True)
    text = models.TextField(verbose_name='Текст статьи', blank=True, null=True)
    data = models.DateField(verbose_name='Дата публикации статьи', auto_now_add=True)
    info = models.URLField(verbose_name='Источник(и)', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    image = models.URLField(verbose_name='Фото', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.id])

    def get_average_rating(self):
        avg = self.ratings.aggregate(Avg('value'))['value__avg']
        return avg if avg else 0

    def get_rating_count(self):
        return self.ratings.count()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Комментарий от {self.author} к {self.article}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        unique_together = ('article', 'user')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    )
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('article', 'user')
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
    
    def __str__(self):
        return f"{self.user.username}: {self.get_value_display()} для {self.article.title}"
