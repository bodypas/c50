from django.urls import path

from . import views

app_name='wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.m_title, name="title"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("new/", views.new, name="new"),
    path("random_page/", views.random_page, name="random_page"),
    path("search/", views.search, name="search"),
   
    
    
        
]
