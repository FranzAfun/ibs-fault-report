from django.urls import path
from .views import PPEIssueCreateView

app_name = 'ppe_records'

urlpatterns = [
    path('new/', PPEIssueCreateView.as_view(), name='ppe-create'),
]
