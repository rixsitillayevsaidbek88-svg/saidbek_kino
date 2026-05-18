from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from movies import views as movie_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie_views.home, name='home'),
    path('movies/', include('movies.urls')),
    path('users/', include('users.urls')),
    path('payments/', include('payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
