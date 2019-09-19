from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('blog/', views.blog, name="post-list"),
    path('create/', views.post_create, name="post-create"),
    path('magazine/', views.magazine, name='magazine'),
    path('contact/', views.contact, name="contact")
]
