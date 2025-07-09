from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Event, Registration
from .forms import EventForm
from accounts.models import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# ListView - mostra eventi disponibili
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registered_events = Registration.objects.filter(attendee=self.request.user).values_list('event_id', flat=True)
        context['registered_event_ids'] = set(registered_events)
        return context


# DetailView - mostra dettagli evento
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

# FUNCTION-BASED VIEW: registrazione evento (Attendee)
@require_POST
@login_required
@permission_required('events.view_event', raise_exception=True)
def register_to_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Registration.objects.get_or_create(attendee=request.user, event=event)
    return redirect('event-list')


# FUNCTION-BASED VIEW: cancellazione registrazione (Attendee)
@require_POST
@login_required
@permission_required('events.view_event', raise_exception=True)
def unregister_from_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Registration.objects.filter(attendee=request.user, event=event).delete()
    return redirect('event-list')

# DashboardView - pagina di redirect dopo il login
@login_required
def dashboard(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_active=True)
    ctx = {
        'is_organizer': user.groups.filter(name='Organizer').exists(),
        'is_attendee': user.groups.filter(name='Attendee').exists(),
        'notifications': notifications,
    }
    return render(request, 'events/dashboard.html', ctx)

# JoinEventView
@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.attendees.add(request.user)
    return redirect('event-list')

# SubscriptionView - mostra gli eventi ai quali si è iscritti
@login_required
def subscriptions_view(request):
    registrations = Registration.objects.filter(attendee=request.user)
    events = [reg.event for reg in registrations]
    return render(request, 'events/subscriptions.html', {'events': events})

# ProfileView - mostra le info del profilo
@login_required
def profile_view(request):
    user = request.user
    group = user.groups.first().name if user.groups.exists() else "None"
    return render(request, 'events/profile.html', {
        'user': user,
        'group': group,
    })

# ManageEventsView - mostra gli eventi creati per un organizer
@login_required
@permission_required('events.add_event', raise_exception=True)
def manage_events_view(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/manage_events.html', {'events': events})

# EventCreateView - solo Organizer può creare eventi
class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    permission_required = 'events.add_event'
    success_url = reverse_lazy('event-list')
    raise_exception = True

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

# DeleteEvent - l'Organizer può cancellare un suo evento
from accounts.models import Notification  # importa il modello notifiche
from django.contrib.auth.models import Group

@login_required
@permission_required('events.delete_event', raise_exception=True)
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == 'POST':
        # Trova tutti gli utenti iscritti (organizer e attendee)
        attendees = event.attendees.all()  # supponendo relazione ManyToMany con nome 'attendees'

        # Crea notifiche per gli utenti iscritti
        message = f'The event "{event.title}" has been deleted.'
        for user in attendees:
            Notification.objects.create(user=user, message=message, is_active=True)

        # Se vuoi notificare anche l’organizer, aggiungilo
        Notification.objects.create(user=event.organizer, message=message, is_active=True)

        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('manage-events')
    return render(request, 'events/confirm_delete.html', {'event': event})

@login_required
@csrf_exempt
def clear_notifications(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_active=True).update(is_active=False)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)