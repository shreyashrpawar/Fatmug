from rest_framework import serializers
from .models import Vendor

class SnippetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    contact_details = serializers.CharField()
    address=serializers.CharField()
    vendor_code=serializers.CharField(max_length=200)
    on_time_delivery_rate=serializers.FloatField(required=False)
    quality_rating_avg=serializers.FloatField(required=False)
    average_response_time=serializers.FloatField(required=False)
    fulfillment_rate=serializers.FloatField(required=False)  

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Vendor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name')
        instance.contact_details = validated_data.get('contact_details')
        instance.address = validated_data.get('address')
        instance.vendor_code = validated_data.get('vendor_code')
        instance.save()
        return instance
    
class PerformanceSerializer(serializers.Serializer):
    vendor_code=serializers.CharField(max_length=200)
    on_time_delivery_rate=serializers.FloatField(required=False)
    quality_rating_avg=serializers.FloatField(required=False)
    average_response_time=serializers.FloatField(required=False)
    fulfillment_rate=serializers.FloatField(required=False)  