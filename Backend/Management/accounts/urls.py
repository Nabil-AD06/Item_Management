from django.urls import path , include
from .views import LoginView  , ProfileUpdateView,ChangePasswordView ,CreateAdminView

urlpatterns = [
    path("login/" , LoginView.as_view() , name="login"),
    # path("test/",TestView.as_view() , name="test"),
    path("profile/",ProfileUpdateView.as_view(),name="profile-update"),
    path("change-password/",ChangePasswordView.as_view(),name="change-password"),
    path("create-admin/",CreateAdminView.as_view(),name="create-admin"),
]