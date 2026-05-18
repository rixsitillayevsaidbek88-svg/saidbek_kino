from django.urls import path
from . import views

urlpatterns = [
    path('premium/', views.premium_page, name='premium'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.premium_success, name='premium_success'),
]
