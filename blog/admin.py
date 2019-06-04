from django.contrib import admin
from .models import Post, Comment
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {'fields': ["title"]}),
        ("Content", {"fields": ["text"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
