from blog.views import PostIndexView, PostDetailView, PostDelete, PostCreate,PostUpdate
from django.urls import path

app_name = 'blog'
urlpatterns = [
    path('', PostIndexView.as_view(), name='post_list'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]
