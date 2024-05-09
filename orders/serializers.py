from rest_framework import serializers
from .models import Orders
from vendors.models import Vendor

class SnippetSerializer(serializers.Serializer):
    po_number = serializers.CharField(max_length=200)
    vendor=serializers.CharField(max_length=200)
    order_date=serializers.DateTimeField()
    delivery_date=serializers.DateTimeField()
    items=serializers.JSONField()
    quantity=serializers.IntegerField()
    status=serializers.CharField()
    quality_rating=serializers.FloatField()
    issue_date=serializers.DateTimeField()
    acknowledgment_date=serializers.DateTimeField(required=False) 

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Orders.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.po_number = validated_data.get('po_number')
        instance.vendor =Vendor.objects.get(vendor_code=validated_data.get('vendor'))
        instance.order_date = validated_data.get('order_date')
        instance.delivery_date = validated_data.get('delivery_date')
        instance.items = validated_data.get('items')
        instance.quantity = validated_data.get('quantity')
        instance.status = validated_data.get('status')
        instance.quality_rating = validated_data.get('quality_rating')
        instance.issue_date = validated_data.get('issue_date')

        instance.save()
        return instance