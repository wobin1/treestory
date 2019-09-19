"""treestories URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static 
from django.conf import settings
from django.contrib import admin
from blog.views import  post, post_update, post_delete
from django.urls import path, include

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('post/<id>/', post, name="post-detail"),
    path('post/<id>/update/', post_update, name="post-update"),
    path('post/<id>/delete/', post_delete, name="post-delete"),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
