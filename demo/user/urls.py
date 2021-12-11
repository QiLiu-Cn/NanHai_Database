from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.reg_view),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('add_note', views.add_note),
    path('home', views.logs),
    path('delete', views.delete_view),
    path('artical', views.artical),
    path('search', views.search)
]