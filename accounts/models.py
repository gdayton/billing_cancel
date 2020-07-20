from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 20)
    email = models.EmailField()

    def __str__(self):
        return self.username

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_agreement_id = models.CharField(max_length = 20)
    authorized = models.BooleanField(default = True)

    def unauthorize(self):
        self.authorized = False
        self.save()

class EmailNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length = 255)
    body = models.TextField()
    sent = models.BooleanField(default = False)