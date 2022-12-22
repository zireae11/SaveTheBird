from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', loginPage, name='login'),
    path('register', registerPage, name='register'),
    path('me', me, name='me'),
    path('logout', doLogout, name='logout'),
    path('downloadfile', views.downloadfile, name='downloadfile'),
   # path('short_url/', views.short_url)
]


