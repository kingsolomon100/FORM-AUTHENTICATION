from django.contrib import admin
from django.urls import path, include
from quickapp import views

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # Main Application Logic
    path('', include('quickapp.urls')),

    # Authentication & User Management
    # We group these under 'accounts/' for a consistent URL structure
    path('accounts/', include([
        path('login/', views.login_view, name='login'),
        path('register/', views.register_view, name='register'),
        path('logout/', views.logout_view, name='logout'),
        path('home/', views.home_view, name='home'),
        path('protected/', views.ProtectedView.as_view(), name='protected'),
        
        # This includes password reset/change views from Django but 
        # lets our custom login/logout take priority above
        path('', include('django.contrib.auth.urls')),
    ])),
]