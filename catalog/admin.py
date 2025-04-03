from django.contrib import admin
from .models import Topic, Article, Comment, Like

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'author', 'data', 'views', 'get_likes_count', 'get_comments_count')
    list_filter = ('topic', 'data', 'author')
    search_fields = ('title', 'summary', 'text')
    date_hierarchy = 'created_at'
    inlines = [CommentInline, LikeInline]
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Лайки'
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    get_comments_count.short_description = 'Комментарии'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at')
    list_filter = ('created_at', 'user')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Настройка заголовка админ-панели
admin.site.site_header = 'ArticleHub - Администрирование'
admin.site.site_title = 'ArticleHub'
admin.site.index_title = 'Панель управления'
