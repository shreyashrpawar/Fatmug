from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from vendors.models import Vendor,Performance
from datetime import datetime
class Orders(models.Model):
    po_number = models.CharField(max_length=200,primary_key=True,unique=True)
    vendor=models.ForeignKey("vendors.Vendor",on_delete=models.CASCADE)
    order_date=models.DateTimeField()
    delivery_date=models.DateTimeField()
    items=models.JSONField()
    quantity=models.IntegerField()
    status=models.CharField(max_length=200)
    quality_rating=models.FloatField()
    issue_date=models.DateTimeField()
    acknowledgment_date=models.DateTimeField(null=True)

    class Meta:
        app_label = 'orders'

    def calculate_on_time_delivery_rate(self):
        completed_orders = Orders.objects.filter(vendor=self.vendor, status='completed')
        on_time_deliveries = completed_orders.filter(delivery_date__lte=models.F('delivery_date')).count()
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0 and on_time_deliveries>0:
            on_time_delivery_rate = on_time_deliveries / total_completed_orders
        else:
            on_time_delivery_rate = 0
        return on_time_delivery_rate

@receiver(post_save, sender=Orders)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    vendor = instance.vendor
    on_time_delivery_rate=0;
    quality_rating_average=0;
    average_response_time=0;
    fulfillment_rate=0;
    if instance.status == 'completed':
        on_time_delivery_rate = instance.calculate_on_time_delivery_rate()
        print(on_time_delivery_rate)
        vendor.on_time_delivery_rate = on_time_delivery_rate
    if instance.status == 'completed':
        completed_orders = Orders.objects.filter(vendor=vendor, status='completed')
        quality_ratings = completed_orders.exclude(quality_rating=None).values_list('quality_rating', flat=True)
        if quality_ratings:
            quality_rating_average = sum(quality_ratings) / len(quality_ratings)
            vendor.quality_rating_avg = quality_rating_average
    if instance.status == 'completed' and instance.acknowledgment_date:
        completed_orders = Orders.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
        response_times = [(order.acknowledgment_date - order.issue_date).total_seconds() for order in completed_orders]
        if response_times:
            average_response_time = sum(response_times) / len(response_times)
            days = average_response_time / (24 * 60 * 60)
            vendor.average_response_time = days
    total_orders = Orders.objects.filter(vendor=vendor).count()
    successful_orders = Orders.objects.filter(vendor=vendor, status='completed', quality_rating__gte=0).count()
    
    if total_orders > 0 and successful_orders>0:
        fulfillment_rate = successful_orders / total_orders
    else:
        fulfillment_rate = 0
    
    vendor.fulfillment_rate = fulfillment_rate
    print(vendor)
    vendor.save()
    if instance.status == 'completed':
        Performance.objects.create(vendor=vendor, date=datetime.now(),on_time_delivery_rate=on_time_delivery_rate,quality_rating_avg=quality_rating_average,average_response_time=average_response_time,fulfillment_rate=fulfillment_rate)