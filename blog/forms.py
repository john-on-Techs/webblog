from django import forms
from tinymce import TinyMCE
from .models import Post


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )

#
# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False
#
#
# class PostForm(forms.ModelForm):
#     content = forms.CharField(
#         widget=TinyMCEWidget(
#             attrs={'required': True, 'cols': 30, 'rows': 10}
#         )
#     )
#
#     class Meta:
#         model = Post
#         fields = ['title', 'text',]



class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, help_text='100 characters max.')
    email = forms.EmailField(required=True)
    comment_message = forms.CharField(widget=forms.Textarea)
