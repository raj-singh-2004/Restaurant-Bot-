from django.urls import path
from . import views



urlpatterns = [
    path('registeruser/',views.registeruser,name='registeruser'),
    path('registerVendor/',views.registerVendor,name="registerVendor"),
]   


