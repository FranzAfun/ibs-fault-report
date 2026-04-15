from django.urls import path
from .views import PPEIssueCreateView, PPEIssueDeleteView, PPEIssueDetailView, PPEIssueListView, PPEIssueUpdateView

app_name = 'ppe_records'

urlpatterns = [
    path('', PPEIssueListView.as_view(), name='ppe-list'),
    path('new/', PPEIssueCreateView.as_view(), name='ppe-create'),
    path('<int:pk>/', PPEIssueDetailView.as_view(), name='ppe-detail'),
    path('<int:pk>/edit/', PPEIssueUpdateView.as_view(), name='ppe-edit'),
    path('<int:pk>/delete/', PPEIssueDeleteView.as_view(), name='ppe-delete'),
]
