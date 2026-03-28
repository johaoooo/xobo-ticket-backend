from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    return JsonResponse({
        'status': 'OK',
        'message': 'Xobo Ticket API is running with Django & PostgreSQL',
        'database': 'PostgreSQL'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health'),
    path('api/auth/', include('users.urls')),
    path('api/stands/', include('stands.urls')),
]

# Servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
