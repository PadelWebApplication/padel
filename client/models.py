from django.db import models
from django.utils import timezone

from userauths import models as userauth_model

NOTIFICATION_TYPE = (
    ("Session Scheduled", "Session Scheduled"),
    ("Session Cancelled", "Session Cancelled"),
)

class Client(models.Model):
    user = models.OneToOneField(userauth_model.User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images", null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}"
    
class Notification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey("base.Session", on_delete=models.CASCADE, null=True, blank=True, 
                                    related_name="client_session_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"{self.client.full_name} Notification"

