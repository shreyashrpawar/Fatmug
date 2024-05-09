from django.shortcuts import render
from django.http import HttpResponse
from .models import Vendor
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
from .serializers import SnippetSerializer,PerformanceSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def new_vendor(request):
  if request.method=='GET':
      data=Vendor.objects.all()
      serializer = SnippetSerializer(data,many=True)
      return Response(serializer.data)
  if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact_details')
        address = request.POST.get('address')
        vendor_code = request.POST.get('vendor_code')
        vendor = Vendor.objects.create(name=name, contact_details=contact, address=address, vendor_code=vendor_code)
        return JsonResponse({'message': 'Vendor created successfully'}, status=201)
  return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['GET','POST','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_details(request,vendor_code):
  try:
        vendor = Vendor.objects.get(vendor_code=vendor_code)
  except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method=='GET':
      serializer = SnippetSerializer(vendor,many=False)
      return Response(serializer.data)
  if request.method == 'POST':
        serializer = SnippetSerializer(vendor,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({'message': 'Vendor updated successfully'}, status=201)
  if request.method == 'DELETE':
        vendor.delete()
        return JsonResponse({'message': 'Vendor Deleted successfully'}, status=201)
  return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request,vendor_code):
  if request.method=='GET':
      vendor = Vendor.objects.get(vendor_code=vendor_code)
      serializer = PerformanceSerializer(vendor,many=False)
      return Response(serializer.data)
  return JsonResponse({'error': 'Invalid request method'}, status=405)