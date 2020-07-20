from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path("billing-cancel-webhook", views.billing_cancel_webhook)
]