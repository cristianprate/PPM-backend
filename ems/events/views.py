from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from .models import Event, Registration
from .forms import EventForm

# 1. ListView - mostra eventi disponibili
class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'


# 2. DetailView - mostra dettagli evento
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


# 3. CreateView - solo Organizer può creare eventi
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

# FUNCTION-BASED VIEW: registrazione evento (Attendee)
@login_required
@permission_required('events.view_event', raise_exception=True)
def register_to_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Registration.objects.get_or_create(attendee=request.user, event=event)
    return redirect('event-detail', pk=event.id)


# FUNCTION-BASED VIEW: cancellazione registrazione (Attendee)
@login_required
@permission_required('events.view_event', raise_exception=True)
def unregister_from_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Registration.objects.filter(attendee=request.user, event=event).delete()
    return redirect('event-detail', pk=event.id)
