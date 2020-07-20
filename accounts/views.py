import json 

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import PaymentMethod, EmailNotification 
from shipments.models import Shipment
from logs.models import Log

from modules.billing import BillingManager

# Create your views here.
@csrf_exempt
def billing_cancel_webhook(request):
    billing_agreement_id = request.POST.get("billing_agreement_id")

    try:
        BillingManager.billing_cancel(billing_agreement_id)
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({
            "error": e.message
        }), content_type="application/json")

    return HttpResponse()