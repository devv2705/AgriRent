from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('shareeq/', views.shareequipment, name='share_eq'),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signout, name='signout'),
    path('renteq/', views.rentequipment, name='rent_eq'),
    path('eid=<str:uid>/', views.equipment_details, name='equipment_details'),
    path('editprofile/', views.editprofile, name='edit_profile'),
    path('myeq/', views.myequipment, name='my_equipment'),
    path('chat/', views.chat, name='chat'),
    path('chat/<str:chat_id>/', views.chat, name='chat_with_id'),  
    path('chat_with_owner/<int:owner_id>/<int:equipment_id>/', views.chat_with_owner, name='chat_with_owner'),  # Use chat_with_owner view here
    path('settings/', views.settings, name='settings'),
    path('send_message/<int:receiver_id>/<int:equipment_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
