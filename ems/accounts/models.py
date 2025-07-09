from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    # Aggiungi campi personalizzati se vuoi
    birth_date = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.username

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_active = models.BooleanField(default=True)  # True = mostra il banner, False = nascosta
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Active: {self.is_active}"