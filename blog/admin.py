from django.contrib import admin
from .models import Post, Comment, Category, Tag
from tinymce.widgets import TinyMCE
from django.db import models
from easy_select2 import select2_modelform

PostForm = select2_modelform(Post, attrs={'width': '350px'})


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('title', 'slug', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'published_at', 'author')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ['published_at', 'status']

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(Category)

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
