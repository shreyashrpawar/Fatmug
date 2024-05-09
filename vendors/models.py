from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact_details = models.TextField()
    address=models.TextField()
    vendor_code=models.CharField(max_length=200,unique=True,primary_key=True)
    on_time_delivery_rate=models.FloatField(null=True)
    quality_rating_avg=models.FloatField(null=True)
    average_response_time=models.FloatField(null=True)
    fulfillment_rate=models.FloatField(null=True)  

class Performance(models.Model):
    vendor=models.ForeignKey("Vendor",on_delete=models.CASCADE)
    date=models.DateTimeField()
    on_time_delivery_rate=models.FloatField(null=True)
    quality_rating_avg=models.FloatField(null=True)
    average_response_time=models.FloatField(null=True)
    fulfillment_rate=models.FloatField(null=True)  