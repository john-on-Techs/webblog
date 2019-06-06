from blog.views import PostIndexView, PostDetailView, PostDelete, PostCreate, PostUpdate, PostDraftView, post_publish, \
    PostComment, comment_approve, comment_remove, TagCreate, contact, about, index
from django.urls import path
from .feeds import PostFeed

app_name = 'blog'
urlpatterns = [
    path('published/', PostIndexView.as_view(), name='post_list'),
    path('drafts/', PostDraftView.as_view(), name='post_draft_list'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('', index, name='home'),
    path('feed/', PostFeed(), name='post_feed'),
    path('tag/create/', TagCreate.as_view(), name='tag-create'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('post/<int:pk>/comment/', PostComment.as_view(), name='post-comment'),
    path('post/<int:pk>/publish/', post_publish, name='post_publish'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post_detail'),


]
