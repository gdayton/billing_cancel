from django.contrib import admin

# Register your models here.
from .models import User, PaymentMethod, EmailNotification

admin.site.register(User)
admin.site.register(PaymentMethod)
admin.site.register(EmailNotification)