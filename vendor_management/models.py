from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
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

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="purchase_orders"
    )
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="pending")
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


from datetime import timedelta


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    """
    Signal handler to update vendor performance metrics when a 
    PurchaseOrder is saved.
    """
    vendor = instance.vendor

    # Update vendor performance metrics here
    total_acknowledged_orders = vendor.purchase_orders.filter(
        acknowledgment_date__isnull=False
    ).count()
    total_response_time_seconds = sum(
        (po.acknowledgment_date - po.issue_date).total_seconds()
        for po in vendor.purchase_orders.filter(acknowledgment_date__isnull=False)
    )
    new_avg_response_time = (
        total_response_time_seconds / total_acknowledged_orders
        if total_acknowledged_orders > 0
        else 0
    )
    # Update the average_response_time field with hours
    vendor.average_response_time = new_avg_response_time
    vendor.save()

