from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    register_to_event,
    unregister_from_event
)

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/create/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:event_id>/register/', register_to_event, name='event-register'),
    path('event/<int:event_id>/unregister/', unregister_from_event, name='event-unregister'),
]