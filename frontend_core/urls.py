from django.urls import path 
from . import views 


# URL configuration module 
urlpatterns = [
    path('home/',views.home_view)
]
