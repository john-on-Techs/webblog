from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from .forms import CommentForm
from .models import Post, Comment, Tag, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

from .forms import ContactForm


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


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


# Create your views here.
def about(request):
    return render(request, 'blog/pages/about.html')


def contact(request):
    title = 'Contact'
    form = ContactForm(request.POST or None)
    confirm_message = "Want to get in touch? Fill out the form below to send " \
                      "me a message and I will get back to you as soon as possible!"
    show_button = True
    if form.is_valid():
        print(request.POST)
        subject = 'Message from MyBlog'
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment_message']
        message = '{name} {comment_message}'.format(name=name, comment_message=comment)
        emailFrom = form.cleaned_data['email']
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, emailFrom, emailTo)
        title = 'Well {name}!.'.format(name=name)
        confirm_message = 'Thank You for the Message.We will get right back to you.'
        form = None
        show_button = False

    context = {'form': form, 'title': title, 'confirm_message': confirm_message, 'show_button': show_button}
    template = 'blog/pages/contact.html'
    return render(request, template, context)


def index(request):
    return render(request, 'blog/base.html')
