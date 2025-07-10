from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    register_to_event,
    unregister_from_event,
    dashboard,
    join_event,
    subscriptions_view,
    profile_view,
    manage_events_view,
    EventCreateView,
    delete_event,
    clear_notifications,
    edit_event_view,
)

urlpatterns = [
        # Dashboard - root path
                path('dashboard/', dashboard, name='dashboard'),

        # Eventi
        path('events/', EventListView.as_view(), name='event-list'),
        path('events/create/', EventCreateView.as_view(), name='event-create'),
        path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
        path('events/<int:event_id>/register/', register_to_event, name='event-register'),
        path('events/<int:event_id>/unregister/', unregister_from_event, name='event-unregister'),
        path('events/<int:pk>/join/', join_event, name='event-join'),
        path('manage/', manage_events_view, name='manage-events'),
        path('event/<int:pk>/delete/', delete_event, name='event-delete'),
        path('clear-notifications/', clear_notifications, name='clear_notifications'),
        path('events/<int:event_id>/edit/', edit_event_view, name='edit_event'),

        # Utente
        path('subscriptions/', subscriptions_view, name='subscriptions'),
        path('profile/', profile_view, name='profile'),
]