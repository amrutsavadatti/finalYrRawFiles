from django.contrib import admin
from django.urls import path
from Forum import views

urlpatterns = [
    path("", views.display, name = "displayPage"),
    path("login", views.login, name = "Login"),
    path("register", views.Register, name = "Register"),
    path("home", views.home, name = "Home"),
]