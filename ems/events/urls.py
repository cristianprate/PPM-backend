from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    register_to_event,
    unregister_from_event,
    dashboard,
    join_event,
    subscriptions_view,
)

urlpatterns = [
        # Homepage → dashboard/menu
        path('', dashboard, name='dashboard'),

        # Eventi
        path('events/', EventListView.as_view(), name='event-list'),
        path('events/create/', EventCreateView.as_view(), name='event-create'),
        path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
        path('events/<int:event_id>/register/', register_to_event, name='event-register'),
        path('events/<int:event_id>/unregister/', unregister_from_event, name='event-unregister'),
        path('events/<int:pk>/join/', join_event, name='event-join'),

        # Utente
        path('subscriptions/', subscriptions_view, name='subscriptions'),
        path('profile/', lambda request: render(request, 'profile.html'), name='profile'),  # placeholder
]