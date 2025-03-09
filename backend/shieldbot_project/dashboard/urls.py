from django.urls import path
from .views import DashboardView, HomeView, TermsView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('home/', HomeView.as_view(), name='home'),
    path('terms/', TermsView.as_view(), name='terms'),
] 