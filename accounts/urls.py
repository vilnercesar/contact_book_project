from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='index_login'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/dashboard/', views.dashboard, name='dashboard'),

]
