"""garbage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url 
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.signIn),
    url(r'^postsign/',views.postsign),
    url(r'^logout/',views.logout,name="log"),
    url(r'^createbin/',views.create_bin,name='create_bin'),
    url(r'^post_create_bin/',views.post_create_bin,name='post_create_bin'),
    url(r'^createdriver/',views.create_driver,name='create_driver'),
    url(r'^post_create_driver/', views.post_create_driver, name="post_create_driver" ),
    url(r'^check/',views.check,name='check'),
    url(r'^check_queries/', views.check_queries, name='check_queries'),
    url(r'^generateroutes/', views.generate_routes, name = 'routes'),
    url(r'^createvehicle/', views.create_vehicle, name = 'vehicles'),
    url(r'^post_create_vehicle/',views.post_create_vehicle,name='post_create_vehicle'),
]
