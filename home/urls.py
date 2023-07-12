from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('shareeq/',views.shareequipment),
    path('profile/',views.profile),
    path('signout/',views.signout),
    path('renteq/',views.search),
    path('eid=<str:uid>/', views.equipment_details),
    path('editprofile/',views.editprofile),
    path('myeq/',views.myequipment),
    path('chat/',views.chat),
    path('chat/<str:chat_id>/',views.chat),
    path('settings/',views.settings),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)