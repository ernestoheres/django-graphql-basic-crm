from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('users', views.users, name='users'),
    path('logout', views.logout, name='logout'),
    path('securepage', views.securepage, name='securepage'),
    path('register', views.register, name='register')
]