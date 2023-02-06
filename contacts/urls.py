from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('contact/<int:id>/', views.contact, name='contact'),
    path('search/', views.search, name='search')


]
