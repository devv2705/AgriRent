from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('sell/',views.shareequipment),
    path('signout/',views.signout),
    path('buy/',views.search),
    path('eid=<str:equipment_id>/', views.equipment_details),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)