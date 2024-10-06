# users/urls.py

from django.urls import path
from .views import RegisterView, LoginView, DashboardView, SearchUsersView, CurrentUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', SearchUsersView.as_view(), name='search-users'),
    path('current/', CurrentUserView.as_view(), name='current-user'),
]
