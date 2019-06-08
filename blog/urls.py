from blog.views import PostCreate, PostDetailView, PostUpdate, PostDelete, PostIndexView, PostDraftView, post_publish, \
    PostComment, comment_approve, comment_remove, contact, about, index, TagListView, TagCreateView, TagUpdateView, \
    TagDetailView, \
    TagDeleteView, CategoryListView, CategoryCreateView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView
from django.urls import path
from .feeds import PostFeed

app_name = 'blog'
urlpatterns = [
    path('published/', PostIndexView.as_view(), name='post-list'),
    path('drafts/', PostDraftView.as_view(), name='post-draft-list'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('', index, name='home'),
    path('feeds/', PostFeed(), name='post-feed'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tag/create/', TagCreateView.as_view(), name='tag-create'),
    path('tag/<int:pk>/delete/', TagDeleteView.as_view(), name='tag-delete'),
    path('tag/<int:pk>/update/', TagUpdateView.as_view(), name='tag-update'),
    path('tag/<str:slug>/', TagDetailView.as_view(), name='tag-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment-remove'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment-approve'),
    path('post/<int:pk>/comment/', PostComment.as_view(), name='post-comment'),
    path('post/<int:pk>/publish/', post_publish, name='post-publish'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post-update'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post-detail'),

]
