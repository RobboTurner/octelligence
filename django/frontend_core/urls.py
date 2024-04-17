from django.urls import path 
from . import views 


# URL configuration module 
urlpatterns = [
    path('',views.home_view),
    path('/handle_search_query',views.handle_search_query,name='handle_search_query')
]
