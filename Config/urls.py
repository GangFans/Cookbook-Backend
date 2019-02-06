"""Config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from Cookbook.views import TagViewSet, CookbookViewSet

router = DefaultRouter()
router.register(r'tag', TagViewSet, basename='tag')
router.register(r'cookbook', CookbookViewSet, basename='cookbook')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('Cookbook.urls', namespace='Book')),

    path('api-auth/', include('rest_framework.urls')),  # 仅仅用于测试
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='Cookbook-Backend API'))
]
