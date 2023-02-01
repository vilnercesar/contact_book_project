from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/<int:id>/', views.contact, name='contact'),


]
