from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, F, Sum


STATUS_CHOICES = [
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]


class Vendor(models.Model):
    """
    Vendor model.
    Represents a vendor entity with information such as name,
    contact details, and address.
    """

    name = models.CharField(max_length=100, null=True, blank=True)
    contact_details = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vendor_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)


class PurchaseOrder(models.Model):
    """
    Purchase Order model.
    Represents a purchase order entity with information such as PO number,
    order date, and status.
    """

    po_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="purchase_orders"
    )
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="pending")
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


from datetime import timedelta


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    """
    Signal handler to update vendor performance metrics when a
    PurchaseOrder is saved.
    """
    if created:  # Only update metrics for newly created Purchase Orders
        vendor = instance.vendor

        # Calculate or retrieve performance metrics based on the Purchase Order data
        on_time_delivery_rate = (
            vendor.purchase_orders.filter(delivery_date__lte=F("delivery_date")).count()
            / vendor.purchase_orders.count()
            * 100
        )  # Calculate on-time delivery rate

        quality_rating_avg = (
            vendor.purchase_orders.aggregate(Avg("quality_rating"))[
                "quality_rating__avg"
            ]
            or 0
        )  # Calculate average quality rating

        total_acknowledged_orders = vendor.purchase_orders.filter(
            acknowledgment_date__isnull=False
        ).count()

        total_response_time_seconds = (
            vendor.purchase_orders.filter(acknowledgment_date__isnull=False).aggregate(
                Sum("vendor__average_response_time")
            )["vendor__average_response_time__sum"]
            or 0
        )

        average_response_time = (
            total_response_time_seconds / total_acknowledged_orders
            if total_acknowledged_orders > 0
            else 0
        )

        fulfillment_rate = (
            vendor.purchase_orders.filter(status="Fulfilled").count()
            / vendor.purchase_orders.count()
            * 100
        )  # Calculate fulfillment rate

        # Create or update HistoricalPerformance record
        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=instance.delivery_date,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate,
        )

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="historical_performance"
    )
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
