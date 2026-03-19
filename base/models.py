from django.db import models

from shortuuid.django_fields import ShortUUIDField

from coach import models as coach_models
from client import models as client_models


class Service(models.Model):
    image = models.FileField(upload_to="images", null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null= True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_coaches = models.ManyToManyField(coach_models.Coach, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cost}"


class Session(models.Model):
    STATUS = [
        ('Scheduled', 'Scheduled'), 
        ('Completed', 'Completed'), 
        ('Pending', 'Pending'), 
        ('Cancelled', 'Cancelled')
    ]
    
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_sessions')
    coach = models.ForeignKey(coach_models.Coach, on_delete=models.SET_NULL, null=True, blank=True, related_name='coach_sessions')
    client = models.ForeignKey(client_models.Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions_client')
    session_date = models.DateTimeField(null=True, blank=True)
    session_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    status = models.CharField(max_length=120, choices=STATUS)

    def __str__(self):
        return f"{self.client.full_name} with {self.coach.full_name}"


class Billing(models.Model):
    client = models.ForeignKey(client_models.Client, on_delete=models.SET_NULL, null=True, blank=True,  related_name='billings')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='billing', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=120, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing for {self.client.full_name} - Total: {self.total}"

