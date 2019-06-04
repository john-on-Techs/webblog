from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm


# Create your views here.
def about(request):
    return render(request, 'profiles/pages/about.html')


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
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
        title = 'Well {name}!.'.format(name=name)
        confirm_message = 'Thank You for the Message.We will get right back to you.'
        form = None
        show_button = False

    context = {'form': form, 'title': title, 'confirm_message': confirm_message,'show_button':show_button}
    template = 'profiles/pages/contact.html'
    return render(request, template, context)


def index(request):
    return render(request, 'profiles/base.html')
