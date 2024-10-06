# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # Include users app URLs
    path('', RedirectView.as_view(url='/api/users/register/')),
    path('api/chat/', include('chat.urls')),
]
