from django.urls import path
from event import views

urlpatterns = [
    path('', views.intro, name="event_title"),
    # Action Member
    path('<str:event_id>/action/', views.actionEvent, name="action_event"),

    # Event 
    path('<str:event_id>', views.getEvent, name="event"),
    path('<str:event_id>/delete/', views.deleteEvent, name="event_delete"),
    path('<str:event_id>/update/', views.updateEvent, name="event_update"),
    path('<str:event_id>/opinion/', views.event_opinion_create, name="event_opinion_create"),
    path('<str:event_id>/opinion-update/<str:opinion_id>', views.event_opinion_update, name="event_opinion_update"),
    path('<str:event_id>/opinion-delete/<str:opinion_id>', views.event_opinion_delete, name="event_opinion_delete"),
    path('create/', views.createEvent, name="create_event"),
    path('all/', views.getAllEvent, name="all_event"),
    path('mine/', views.myEvent, name="my_event"),
    path('auth_all/', views.authAllEvent, name="author_all_event"),
    path('author/', views.authorEvent, name="author_event"),
    path('eventfile-upload', views.uploadEventFile, name="upload-event-photo"),
]