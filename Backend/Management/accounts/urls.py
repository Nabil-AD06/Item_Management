from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    ProfileUpdateView,
    ChangePasswordView,
    CreateAdminView,
    CreateRequestView,
    RequestListView,
    RequestDetailView,
    RequestItemDeleteView,
    EquipmentListCreateView,
    EquipmentDetailView,
    CategoryViewSet,
)

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("login/" , LoginView.as_view() , name="login"),
    # path("test/",TestView.as_view() , name="test"),
    path("profile/",ProfileUpdateView.as_view(),name="profile-update"),
    path("change-password/",ChangePasswordView.as_view(),name="change-password"),
    path("create-admin/",CreateAdminView.as_view(),name="create-admin"),
    path("create-request/",CreateRequestView.as_view(),name="create-request"),
    path("requests/",RequestListView.as_view(),name="requests"),
    path("requests/<int:pk>/",RequestDetailView.as_view(),name="request-detail"),
    path("request-items/<int:pk>/",RequestItemDeleteView.as_view(),name="request-item-delete"),
    path("equipment/",EquipmentListCreateView.as_view(),name="equipment-list-create"),
    path("", include(router.urls)),
    path("equipment/<int:pk>/", EquipmentDetailView.as_view(), name="equipment-detail"),
]