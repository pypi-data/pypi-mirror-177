import logging

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ob_dj_store.core.stores.gateway.tap.managers import TapPaymentManager

logger = logging.getLogger(__name__)


class TapPayment(models.Model):
    """TapPayment captures the payment from Tap"""

    class Status(models.TextChoices):
        INITIATED = "INITIATED"
        IN_PROGRESS = "IN_PROGRESS"
        ABANDONED = "ABANDONED"
        CANCELLED = "CANCELLED"
        FAILED = "FAILED"
        DECLINED = "DECLINED"
        RESTRICTED = "RESTRICTED"
        CAPTURED = "CAPTURED"
        VOID = "VOID"
        TIMEDOUT = "TIMEDOUT"
        UNKNOWN = "UNKNOWN"

    class Sources(models.TextChoices):
        CREDIT_CARD = "src_card", _("Credit Card")
        KNET = "src_kw.knet", _("KNet")
        ALL = "src_all", _("All")

    status = models.CharField(max_length=100, choices=Status.choices)
    source = models.CharField(max_length=100, choices=Sources.choices)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        help_text=_(
            "Captured the User ID for both registered "
            "users and Guests (Every guest user has a user_id assigned by device_id)"
        ),
    )
    langid = models.CharField(
        max_length=10,
        help_text=_(
            "Capture language for debugging & analytical only purposes (ARA for Arabic & ENG for English)"
        ),
    )
    payment = models.OneToOneField(
        "stores.Payment",
        on_delete=models.CASCADE,
        related_name="tap_payment",
        help_text=_("Reference local payment transaction table"),
    )
    result = models.CharField(
        max_length=100, help_text=_("Status response from TAP gateway")
    )
    # payment details
    payment_url = models.CharField(
        max_length=250, help_text=_("Captures generated URL for user payment")
    )
    charge_id = models.CharField(
        max_length=250,
        help_text=_("Charge ID returned from TAP"),
        unique=True,
        db_index=True,
    )
    init_response = models.JSONField(
        help_text=_("Response received when initiating the payment"),
        null=True,
        blank=True,
    )
    callback_response = models.JSONField(
        help_text=_("Callback response received after the payment is done"),
        null=True,
        blank=True,
    )
    # audit fields
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("Datetime when payment was initiated"),
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    objects = TapPaymentManager()

    class Meta:
        verbose_name = _("TAP Payment")

    @property
    def amount(self):
        return self.payment.amount

    def callback_update(self, tap_payload):
        if self.status == self.Status.INITIATED:
            self.result = tap_payload["status"]
            self.callback_response = tap_payload
            self.status = tap_payload["status"]
            self.save()
            self.mark_transaction()
            logger.info(f"Mark TAP Transaction finished for charge ID {self.charge_id}")

    def mark_transaction(self):
        if self.status == self.Status.CAPTURED:
            self.payment.mark_paid()
        elif self.status == self.Status.FAILED:
            self.payment.mark_failed()
