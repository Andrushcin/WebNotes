from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('notes.urls')),
    path('notes/', include('notes.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('info/', include('info.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
