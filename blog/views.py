from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).order_by('published_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)


# ----Class Based Views-------
class PostIndexView(generic.ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.filter(published_at__lte=timezone.now()).order_by('published_at')


class PostDraftView(LoginRequiredMixin,generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.filter(published_at__isnull=True).order_by('created_at')


class PostDetailView(generic.DetailView):
    model = Post


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
