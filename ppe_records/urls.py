from django.urls import path
from .views import PPEIssueCreateView, PPEIssueDeleteView, PPEIssueDetailView, PPEIssueListView, PPEIssueUpdateView, sign_ppe_item

app_name = 'ppe_records'

urlpatterns = [
    path('', PPEIssueListView.as_view(), name='ppe-list'),
    path('new/', PPEIssueCreateView.as_view(), name='ppe-create'),
    path('<int:pk>/', PPEIssueDetailView.as_view(), name='ppe-detail'),
    path('<int:pk>/update/', PPEIssueUpdateView.as_view(), name='ppe-update'),
    path('<int:pk>/edit/', PPEIssueUpdateView.as_view(), name='ppe-edit'),
    path('item/<int:item_id>/sign/', sign_ppe_item, name='ppe-sign'),
    path('<int:pk>/delete/', PPEIssueDeleteView.as_view(), name='ppe-delete'),
]
