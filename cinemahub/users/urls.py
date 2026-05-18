from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('save-movie/<int:movie_id>/', views.save_movie, name='save_movie'),
    path('send-movie/<int:movie_id>/', views.send_movie, name='send_movie'),
]
