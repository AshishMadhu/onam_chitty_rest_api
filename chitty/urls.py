from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls', namespace = "user")),
    path('', include('onam_chitty.urls', namespace = "onam_chitty")),
]
