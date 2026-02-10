from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),

    # API
    path('api/register/', views.api_register),
    path('api/login/', views.api_login),
    path('api/logout/', views.api_logout),
    path('api/reset-password/', views.api_reset_password),

    # Reminder
    path('add-reminder/', views.add_reminder, name='add_reminder'),
    path('delete/<int:id>/', views.delete_reminder, name='delete'),
    path('taken/<int:id>/', views.mark_taken, name='taken'),
    path('edit/<int:id>/', views.edit_reminder, name='edit'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # more api 
    path('api/add-reminder/', views.api_add_reminder),
    path('api/reminders/', views.api_reminders),
    path('api/delete/<int:id>/', views.api_delete),
    path('api/taken/<int:id>/', views.api_taken),

    path('api/profile/', views.api_profile),
    path('api/profile-update/', views.api_profile_update),

]

# MEDIA FILES (profile photo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
