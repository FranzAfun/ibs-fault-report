from django.urls import path

from .views import (
    CheckbookCreateView,
    CheckbookDeleteView,
    CheckbookDetailView,
    CheckbookListView,
    CheckbookUpdateView,
)

app_name = 'checkbook'

urlpatterns = [
    path('', CheckbookListView.as_view(), name='list'),
    path('new/', CheckbookCreateView.as_view(), name='create'),
    path('<int:pk>/', CheckbookDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', CheckbookUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', CheckbookDeleteView.as_view(), name='delete'),
]
