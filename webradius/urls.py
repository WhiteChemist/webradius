"""webradius URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from cgitb import handler
from logging import handlers
from django.contrib import admin
from django.urls import path
from radius.views import index,handler404,adduser,updateuser,deleteuser



urlpatterns = [
    path('',index,name="index"),
    path('templates/adduser_page.html',adduser,name="adduser"),
    path('templates/updateuser_page.html',updateuser,name="updateuser"),
    path('templates/deleteuser_page.html',deleteuser,name="deleteuser"),
    path('templates/addgroup_page.html',adduser,name="addgroup"),
    path('templates/updategroup_page.html',adduser,name="updategroup"),
    path('templates/deletegroup_page.html',adduser,name="deletegroup"),
    path('admin/', admin.site.urls)
]

handler404=handler404