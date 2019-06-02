from blog.views import PostIndexView, PostDetailView, PostDelete, PostCreate, PostUpdate, PostDraftView,post_publish
from django.urls import path

app_name = 'blog'
urlpatterns = [

    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('post/<int:pk>/publish', post_publish, name='post_publish'),
    path('post/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('drafts/', PostDraftView.as_view(), name='post_draft_list'),
    path('', PostIndexView.as_view(), name='post_list'),
]
