import datetime
from django.test import TestCase
from django.utils import timezone

from accounts.models import User, PaymentMethod, EmailNotification
from shipments.models import Shipment
from logs.models import Log

from modules.billing import BillingManager

# Create your tests here.
class BillingTestCase(TestCase):
    def setUp(self):
        self.USERNAME = "batman"
        self.EMAIL = "batman@gmail.com"
        self.BILLING_AGREEMENT_ID = 1234
        self.CURRENT_DATETIME = timezone.now()

        self.user = User.objects.create(
            username=self.USERNAME,
            email=self.EMAIL
        )
        self.payment_method = PaymentMethod.objects.create(
            user=self.user, 
            billing_agreement_id=self.BILLING_AGREEMENT_ID, 
            authorized=True
        )
        self.shipment = Shipment.objects.create(
            user=self.user, 
            date=self.CURRENT_DATETIME, 
            sent=False
        )

    def test_billing_cancel_nominal(self):
        billing_cancel = BillingManager.billing_cancel(self.BILLING_AGREEMENT_ID)
        
        # check that payment was unauthorized
        self.assertFalse(PaymentMethod.objects.get(billing_agreement_id=self.BILLING_AGREEMENT_ID).authorized)
        
        # check that a log was made
        self.assertTrue(Log.objects.all().exists())

        # check that an email notification was made
        self.assertTrue(EmailNotification.objects.all().exists())

        # check that pendings shipments were removed
        self.assertFalse(Shipment.objects.all().exists())

        # check that billing_cancel result is True
        self.assertTrue(billing_cancel)

    # test_billing_cancel_no_billing_agreement_id
    # test_billing_cancel_not_found_billing_agreement_id
    # test_billing_cancel_off_nominal_billing_agreement_id_bad_object
    # test_remove_pending_shipments_by_user
    # test_remove_pending_shipments_by_user_no_user
    # test_remove_pending_shipments_by_user_no_associated_user
    # test_remove_pending_shipments_by_user_off_nominal_bad_object
    