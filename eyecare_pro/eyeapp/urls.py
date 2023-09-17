from django.contrib import admin
from .import views
from django.urls import path
from eyeapp import views 

urlpatterns = [
    path('', views.index,name='index'),
    # path('cc', views.cc,name='cc'),
    # path('dd', views.dd,name='dd'),
    # path('about/',views.about,name="about"),
    
     
]
