from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('UserProfile/', include('UserProfile.urls')),
    path('extract/', include('extract.urls')),
    path('planning/', include('planning.urls')),
    path('bill/', include('bill.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
