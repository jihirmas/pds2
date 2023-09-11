
from django.contrib import admin
from django.urls import include, path
from its.views import index, CustomLoginView

urlpatterns = [
    path('', include('its.urls')),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    
    
]
