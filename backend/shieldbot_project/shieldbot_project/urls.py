"""
URL configuration for shieldbot_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import TestListCreateAPIView, csrf_token_view
from accounts.views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    PasswordResetView,
    VerifyTokenView,
    RefreshTokenView
)
from attacks.views import (
    PerformTestView,
    TestStatusView,
    ListTestsView,
    StartAttackView,
    StopDDoSView,
    StopAllDDoSView,
    GetCommandView,
    ExecuteAttackView
)
from dashboard.views import DashboardView, HomeView, TermsView

from accounts.views import UserRegistrationView, UserLoginView, UserLogoutView, PasswordResetView, VerifyTokenView, RefreshTokenView
from api.views import TestListAPIView  # or TestListCreateAPIView if you allow creation via API
from dashboard.views import DashboardView, HomeView, TermsView
from attacks.views import StartAttackView  # and other views if needed

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('auth/reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('auth/verify-token/', VerifyTokenView.as_view(), name='verify-token'),
    path('auth/refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),

    # JWT endpoints (if using SimpleJWT directly)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Available tests endpoint
    path('api/tests/', TestListAPIView.as_view(), name='test-list'),
    path('api/get-csrf/', csrf_token_view, name='get-csrf'),


    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # Optionally, add a home route for the dashboard:
    path('dashboard/home/', HomeView.as_view(), name='dashboard-home'),
    path('dashboard/terms/', TermsView.as_view(), name='dashboard-terms'),

    # Attack execution endpoint
    path('attack/start/', StartAttackView.as_view(), name='start-attack'),]
