from django.urls import path
from . import views

urlpatterns = [
    # path('signin/', views.signin),
    # path('signup/', views.signup),
    # path('verify_otp/', views.verify_otp),
    path("home/",views.home),
    path('ShareEquipment/',views.shareequipment),
    path('search/',views.search),
    path('rentequipment',views.rentequipment),
]
