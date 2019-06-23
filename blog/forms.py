from django import forms
from tinymce import TinyMCE
from .models import Post, Tag, Category


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    text = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': True, 'cols': 30, 'rows': 10}
        )
    )


class PostForm(forms.ModelForm):
    text = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': True, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'tags', 'category', 'text']


class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, help_text='100 characters max.')
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
