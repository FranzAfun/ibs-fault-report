from django.urls import path

from .views import (
    AssetFaultAssignView,
    AssetFaultCreateView,
    AssetFaultDeleteView,
    AssetFaultDetailView,
    AssetFaultListView,
    AssetFaultResolveView,
    AssetFaultSignView,
    AssetFaultUpdateView,
)

app_name = 'asset_faults'

urlpatterns = [
    path('', AssetFaultListView.as_view(), name='list'),
    path('new/', AssetFaultCreateView.as_view(), name='create'),
    path('<int:pk>/', AssetFaultDetailView.as_view(), name='detail'),
    path('<int:pk>/assign/', AssetFaultAssignView.as_view(), name='assign'),
    path('<int:pk>/sign/', AssetFaultSignView.as_view(), name='sign'),
    path('<int:pk>/resolve/', AssetFaultResolveView.as_view(), name='resolve'),
    path('<int:pk>/edit/', AssetFaultUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AssetFaultDeleteView.as_view(), name='delete'),
]