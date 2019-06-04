from django.urls import path
from .views import index, contact,about

app_name = 'profiles'
urlpatterns = [
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('', index, name='index')
]
