from django.urls import path , include
from .views import LoginView,ProfileUpdateView,ChangePasswordView,CreateAdminView,CreateRequestView,RequestListView,RequestUpdateView

urlpatterns = [
    path("login/" , LoginView.as_view() , name="login"),
    # path("test/",TestView.as_view() , name="test"),
    path("profile/",ProfileUpdateView.as_view(),name="profile-update"),
    path("change-password/",ChangePasswordView.as_view(),name="change-password"),
    path("create-admin/",CreateAdminView.as_view(),name="create-admin"),
    path("create-request/",CreateRequestView.as_view(),name="create-request"),
    path("requests/",RequestListView.as_view(),name="requests"),
    path("requests/<int:pk>/", RequestUpdateView.as_view()),
]