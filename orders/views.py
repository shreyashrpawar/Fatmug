from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from .models import Orders
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
from .serializers import SnippetSerializer
from vendors.models import Vendor
from datetime import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def new_order(request):
  if request.method=='GET':
      data=Orders.objects.all()
      serializer = SnippetSerializer(data,many=True)
      return Response(serializer.data)
  if request.method == 'POST':
        po_number = request.POST.get('po_number')
        vendor =Vendor.objects.get(vendor_code=request.POST.get('vendor')) 
        order_date = request.POST.get('order_date')
        delivery_date = request.POST.get('delivery_date')
        items = request.POST.get('items')
        quantity = request.POST.get('quantity')
        status = request.POST.get('status')
        quality_rating = request.POST.get('quality_rating')
        issue_date = request.POST.get('issue_date')        
        order = Orders.objects.create(po_number=po_number, vendor=vendor, order_date=order_date, delivery_date=delivery_date,items=items,quantity=quantity,status=status,quality_rating=quality_rating,issue_date=issue_date,)
        return JsonResponse({'message': 'Vendor created successfully'}, status=201)
  return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['GET','POST','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def po_details(request,po_number):
  try:
        order = Orders.objects.get(po_number=po_number)
  except order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method=='GET':
      serializer = SnippetSerializer(order,many=False)
      return Response(serializer.data)
  if request.method == 'POST':
        
        serializer = SnippetSerializer(order,data=request.data)
        print(serializer)
        if serializer.is_valid():
            print("not valid")
            serializer.save()
        return JsonResponse({'message': 'Order updated successfully'}, status=201)
  if request.method == 'DELETE':
        order.delete()
        return JsonResponse({'message': 'Vendor Deleted successfully'}, status=201)
  return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge(request,po_number):
     if request.method=='GET':
            data=Orders.objects.get(po_number=po_number)
            current=datetime.now()
            data.acknowledgment_date=current
            data.save()
            return JsonResponse({'message':'Order acknowledged'},status=201)