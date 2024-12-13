from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms/', include('web.cms.urls')),
    path('auth/', include('web.auth.urls')),
    path('profile/', include('web.profile.urls')),
    path('events/', include('web.events.urls')),
    path('', include('web.home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
