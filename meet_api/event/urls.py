from django.urls import path
from event import views

urlpatterns = [
    path('', views.intro, name="Event"),
    
]