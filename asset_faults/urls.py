from django.urls import path

from .views import (
    AssetFaultCreateView,
    AssetFaultDeleteView,
    AssetFaultDetailView,
    AssetFaultListView,
    AssetFaultSignView,
    AssetFaultUpdateView,
)

app_name = 'asset_faults'

urlpatterns = [
    path('', AssetFaultListView.as_view(), name='list'),
    path('new/', AssetFaultCreateView.as_view(), name='create'),
    path('<int:pk>/', AssetFaultDetailView.as_view(), name='detail'),
    path('<int:pk>/sign/', AssetFaultSignView.as_view(), name='sign'),
    path('<int:pk>/edit/', AssetFaultUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AssetFaultDeleteView.as_view(), name='delete'),
]