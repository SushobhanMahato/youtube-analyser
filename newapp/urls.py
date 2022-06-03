from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), #first page or home page
    path("home", views.home, name='home'),#Main Application page
    path("generate", views.generate, name='generate'),#Function to generate perticuler set of values for given input
]
