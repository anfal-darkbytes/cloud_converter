from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cloudConverterApp.urls')),
    path('', include('blog.urls.web_urls')),
    path('tynymce/', include('tinymce.urls')),
    path('', include('accounts.urls')),

    # API's
    path('api/', include('api.urls'))

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)