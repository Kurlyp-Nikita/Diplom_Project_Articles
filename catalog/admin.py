from django.contrib import admin
from .models import *

admin.site.register(Topic)


@admin.register(Sience)
class SienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'author')
    list_filter = ('topic', )


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'author')
    list_filter = ('topic', )


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'author')
    list_filter = ('topic', )
