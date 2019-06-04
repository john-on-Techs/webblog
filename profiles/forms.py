from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, help_text='100 characters max.')
    email = forms.EmailField(required=True)
    comment_message = forms.CharField(widget=forms.Textarea)
