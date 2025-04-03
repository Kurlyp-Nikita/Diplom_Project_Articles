from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topic, Article, Comment, Like

# Create your tests here.

class TopicModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name=Topic.SCIENCE)
    
    def test_topic_name(self):
        self.assertEqual(str(self.topic), 'Наука')

class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(name=Topic.SCIENCE)
        self.article = Article.objects.create(
            topic=self.topic,
            title='Тестовая статья',
            summary='Краткое описание',
            text='Полный текст статьи',
            author=self.user,
            info='https://example.com'
        )
    
    def test_article_string_representation(self):
        self.assertEqual(str(self.article), 'Тестовая статья')
    
    def test_get_absolute_url(self):
        self.assertEqual(self.article.get_absolute_url(), reverse('article_detail', args=[self.article.id]))
    
    def test_article_fields(self):
        self.assertEqual(self.article.title, 'Тестовая статья')
        self.assertEqual(self.article.summary, 'Краткое описание')
        self.assertEqual(self.article.text, 'Полный текст статьи')
        self.assertEqual(self.article.author, self.user)
        self.assertEqual(self.article.views, 0)

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(name=Topic.SCIENCE)
        self.article = Article.objects.create(
            topic=self.topic,
            title='Тестовая статья',
            author=self.user
        )
        self.comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            text='Тестовый комментарий'
        )
    
    def test_comment_string_representation(self):
        self.assertEqual(str(self.comment), f'Комментарий от {self.user} к {self.article}')

class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(name=Topic.SCIENCE)
        self.article = Article.objects.create(
            topic=self.topic,
            title='Тестовая статья',
            author=self.user
        )
        self.like = Like.objects.create(
            article=self.article,
            user=self.user
        )
    
    def test_like_unique_constraint(self):
        """Проверяем, что нельзя создать дублирующийся лайк"""
        with self.assertRaises(Exception):
            Like.objects.create(
                article=self.article,
                user=self.user
            )
