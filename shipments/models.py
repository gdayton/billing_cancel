from django.db import models

from accounts.models import User

# Create your models here.

class Shipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    sent = models.BooleanField(default=False)