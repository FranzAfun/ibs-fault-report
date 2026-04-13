from django.urls import path

from .views import (
    FaultReportCreateView,
    FaultReportDeleteView,
    FaultReportDetailView,
    FaultReportListView,
    FaultReportUpdateView,
)

app_name = 'fault_logs'

urlpatterns = [
    path('', FaultReportListView.as_view(), name='faultreport-list'),
    path('new/', FaultReportCreateView.as_view(), name='faultreport-create'),
    path('<int:pk>/', FaultReportDetailView.as_view(), name='faultreport-detail'),
    path('<int:pk>/edit/', FaultReportUpdateView.as_view(), name='faultreport-update'),
    path('<int:pk>/delete/', FaultReportDeleteView.as_view(), name='faultreport-delete'),
]
