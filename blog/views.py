from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib.messages.views import messages

from .models import Post, Comment, Tag, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CommentForm,ContactForm, TagForm, CategoryForm,PostForm



# CRUD OPERATIONS FOR CATEGORY MODEL
class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'categories'
    paginate_by = 5
    template_name = 'blog/category/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryForm
        return context

    def post(self, *args, **kwargs):
        try:
            Category(name=self.request.POST['name']).save()
            messages.success(self.request, "Category added successfully")
            return redirect('blog:category-list')
        except:
            raise ValueError("Slug Field already exists")


class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Category
    fields = ['name']
    success_message = "%(name)s was created successfully"
    template_name = 'blog/category/category_form.html'


class CategoryDetailView(generic.DetailView):
    model = Category
    query_pk_and_slug = True
    template_name = 'blog/category/category_detail.html'


class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Category
    fields = ['name']
    success_message = "%(name)s was updated successfully"
    template_name = 'blog/category/category_form.html'


class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Category
    template_name = 'blog/category/category_confirm_delete.html'
    success_message = "%(title)s was deleted successfully"
    success_url = reverse_lazy('blog:category-list')


# CRUD OPERATIONS FOR TAG MODEL
class TagListView(generic.ListView):
    model = Tag
    context_object_name = 'tags'
    paginate_by = 5
    template_name = 'blog/tag/tag_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TagForm
        return context

    def post(self, request, *args, **kwargs):
        try:
            Tag(name=self.request.POST['name']).save()
            messages.success(self.request, "Tag added successfully")
            return redirect('blog:tag-list')
        except:
            raise ValueError("Slug Field already exists")


class TagCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Tag
    fields = ['name']
    success_message = "%(name)s was created successfully"
    template_name = 'blog/tag/tag_form.html'


class TagDetailView(generic.DetailView):
    model = Tag
    query_pk_and_slug = True
    template_name = 'blog/tag/tag_detail.html'


class TagUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Tag
    fields = ['name']
    success_message = "%(name)s was updated successfully"
    template_name = 'blog/tag/tag_form.html'


class TagDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Tag
    template_name = 'blog/tag/tag_confirm_delete.html'
    success_message = "%(title)s was deleted successfully"
    success_url = reverse_lazy('blog:tag-list')


# CRUD OPERATIONS VIEWS FOR POST MODEL
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post-detail', slug=post.slug)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post-detail', slug=comment.post.slug)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post-detail', slug=comment.post.slug)


class PostComment(SuccessMessageMixin, generic.CreateView):
    model = Comment
    fields = ['author', 'text', ]

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post-detail', kwargs={'slug': self.object.post.slug})


# ----Class Based Views-------
class PostIndexView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Post.objects.filter(published_at__lte=timezone.now()).order_by('published_at')
        return Post.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:6]
        context['tags'] = Tag.objects.all()[:6]
        return context


class PostDraftView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post/post_draft_list.html'
    paginate_by = 3

    def get_queryset(self):
        """Return the last five published questions."""

        return Post.drafts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:6]
        context['tags'] = Tag.objects.all()[:6]
        return context


class PostDetailView(generic.DetailView):
    model = Post
    query_pk_and_slug = True
    template_name = 'blog/post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


class PostCreate(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    success_message = "%(title)s was created successfully"
    template_name = 'blog/post/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Blog Post"
        return context


class PostUpdate(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    form_class = PostForm

    query_pk_and_slug = True
    success_message = "%(title)s was updated successfully"
    template_name = 'blog/post/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Blog Post"
        return context


class PostDelete(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Post
    success_message = "%(title)s was deleted successfully"
    success_url = reverse_lazy('blog:post-list')
    template_name = 'blog/post/post_confirm_delete.html'


# PROFILE VIEWS.
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
