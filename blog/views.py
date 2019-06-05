from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from .forms import CommentForm
from .models import Post, Comment, Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    post.status = 'published'
    return redirect('blog:post_detail', slug=post.slug)


def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', slug=comment.post.slug)


class PostComment(generic.CreateView):
    model = Comment
    fields = ['author', 'text', ]

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.post.slug})


# ----Class Based Views-------
class PostIndexView(generic.ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Post.objects.filter(published_at__lte=timezone.now()).order_by('published_at')
        return Post.published.all()


class PostDraftView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        """Return the last five published questions."""

        return Post.drafts.all()


class PostDetailView(generic.DetailView):
    model = Post
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'tags', 'category', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Blog Post"
        return context


class TagCreate(generic.CreateView):
    model = Tag
    fields = ['name', 'posts']


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'tags', 'category', 'text']
    query_pk_and_slug = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Blog Post"
        return context


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
