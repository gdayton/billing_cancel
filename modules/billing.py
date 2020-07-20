from accounts.models import PaymentMethod, EmailNotification 
from shipments.models import Shipment
from logs.models import Log

class BillingException(Exception):
    def __init__(self, message):
        self.message = message

class BillingManager():
    def unauthorize_payment_method(billing_agreement_id):
        try:
            payment_method = PaymentMethod.objects.get(billing_agreement_id=billing_agreement_id)
            payment_method.unauthorize()

            return payment_method.user
        except PaymentMethod.DoesNotExist:
            raise BillingException("Payment method for billing_agreement_id = %s could not be found" % billing_agreement_id)
        except Exception:
            raise BillingException("Error unauthorizing payment method")

    def remove_pending_shipments_by_user(user):
        try:
            Shipment.objects.filter(user=user, sent=False).delete()
        except Exception:
            raise BillingException("Error removing shipments sent by user")

    def billing_cancel(billing_agreement_id):
        if billing_agreement_id is None:
            raise BillingException("Missing billing_agreement_id")

        # 1) Unauthorize payment method
        user = BillingManager.unauthorize_payment_method(billing_agreement_id)
        
        # 2) Create a new Log w/ user from payment method
        Log.objects.create(
            user=user, 
            message="Payment method associated with billing_agreement_id has been unauthorized."
        )

        # 3) Create a EmailNotification object w/ arb message
        EMAIL_SUBJECT = "Billing Agreement Cancellation"
        EMAIL_BODY = "%s, Your billing agreement has been canceled, and your payment method has been unauthorized. -Literati"
        EmailNotification.objects.create(
            user=user,
            subject=EMAIL_SUBJECT,
            body=EMAIL_BODY % user
        )

        # 4) Delete any sent shipments sent by user
        BillingManager.remove_pending_shipments_by_user(user)

        return True