from account import views
from django.urls import path

urlpatterns = [
    path('', views.get_profile, name="profile"),
    path('<str:username>', views.get_profile_username, name="profile-username"),
    path('profileupload/', views.uploadProfileImage, name="profile-pic-upload"),
    path('admin/all/', views.get_allprofile, name="all-profile"),
    path('update-profile/', views.update_profile, name="update-profile"),
]