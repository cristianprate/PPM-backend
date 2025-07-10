from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from .models import CustomUser
from events.models import Event

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # salva l'utente nel DB
        self.object = form.save()

        # assegna il gruppo in base al role scelto
        role = form.cleaned_data.get('role')
        if role:
            group, _ = Group.objects.get_or_create(name=role)
            self.object.groups.add(group)

        # fai login all'utente appena creato
        login(self.request, self.object)

        # redirect alla pagina di successo
        return redirect(self.success_url)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')