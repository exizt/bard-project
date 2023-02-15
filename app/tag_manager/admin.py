from django.contrib import admin
from .models import *


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'count', 'parent')
    search_fields = ('name',)
    readonly_fields = ('count', 'slug')
