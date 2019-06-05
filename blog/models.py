from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from tinymce import HTMLField


# Create your models here.
# Custom Manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class DraftsManager(models.Manager):
    def get_queryset(self):
        return super(DraftsManager, self).get_queryset().filter(status='draft')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    # The default Manager
    objects = models.Manager()

    # Custom Manager
    published = PublishedManager()
    drafts = DraftsManager()

    class Meta:
        ordering = ('-published_at',)
        index_together = (('id', 'slug'),)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
