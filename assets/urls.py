from django.urls import path
from .views import (
	AssetRecordListView,
	AssetRecordCreateView,
	AssetRecordDetailView,
	AssetRecordUpdateView,
	AssetRecordDeleteView,
	AssetItemSignView,
)

app_name = 'assets'

urlpatterns = [
	path('', AssetRecordListView.as_view(), name='asset-list'),
	path('new/', AssetRecordCreateView.as_view(), name='asset-create'),
	path('<int:pk>/', AssetRecordDetailView.as_view(), name='asset-detail'),
	path('<int:pk>/edit/', AssetRecordUpdateView.as_view(), name='asset-update'),
	path('<int:pk>/delete/', AssetRecordDeleteView.as_view(), name='asset-delete'),
	path('items/<int:item_id>/sign/', AssetItemSignView.as_view(), name='asset-sign'),
]
