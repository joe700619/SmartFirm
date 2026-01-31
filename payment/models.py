from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

class PaymentProvider(models.Model):
    """
    Configuration for Payment Providers (e.g., ECPay, LINE Pay).
    """
    name = models.CharField(_("Provider Name"), max_length=50)
    code = models.SlugField(_("Provider Code"), max_length=50, unique=True, help_text="Unique identifier, e.g., 'ecpay'")
    is_active = models.BooleanField(_("Is Active"), default=True)
    config = models.JSONField(_("Configuration"), default=dict, blank=True, help_text="API Keys, Merchant IDs, etc.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PaymentTransaction(models.Model):
    """
    Records a payment attempt.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        SUCCESS = 'SUCCESS', _('Success')
        FAILED = 'FAILED', _('Failed')
        REFUNDED = 'REFUNDED', _('Refunded')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(PaymentProvider, on_delete=models.PROTECT, related_name='transactions')
    
    # Internal unique ID for the trade (e.g., sent to ECPay as MerchantTradeNo)
    merchant_trade_no = models.CharField(_("Merchant Trade No"), max_length=64, unique=True)
    
    # External ID from the provider (e.g., TradeNo from ECPay)
    trade_no = models.CharField(_("Provider Trade No"), max_length=64, blank=True, null=True)
    
    amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=0, help_text="TWD usually has no decimals")
    currency = models.CharField(_("Currency"), max_length=3, default='TWD')
    
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Polymorphic relation to the source order (RegistrationCase, BookingOrder, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    payment_time = models.DateTimeField(_("Payment Time"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    response_data = models.JSONField(_("Response Data"), default=dict, blank=True, help_text="Full response from provider")

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Payment Transaction")
        verbose_name_plural = _("Payment Transactions")

    def __str__(self):
        return f"{self.merchant_trade_no} ({self.status})"
