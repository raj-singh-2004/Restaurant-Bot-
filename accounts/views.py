from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .serializers import UserRegisterSerializer,VendorRegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import io
from .models import User,UserProfile
from rest_framework import status
from django.db import transaction
# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def registeruser(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data) 
        if serializer.is_valid():
            user = serializer.save()
            user.role = User.CUSTOMER
            user.save()
            return Response({"success": True, "data": serializer.data, "error": None},status=status.HTTP_201_CREATED,)
        else:
            return Response({"success": False,"data": None, "error": serializer.errors},status=status.HTTP_400_BAD_REQUEST,)

@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])  # needed for vendor_license file
def registerVendor(request):
    if request.method =="POST":
        user_serializer = UserRegisterSerializer(data=request.data)
        vendor_serializer = VendorRegisterSerializer(data=request.data)

        if user_serializer.is_valid() and vendor_serializer.is_valid():
            with transaction.atomic():
                user = user_serializer.save()
                user.role = User.VENDOR
                user.save(update_fields=["role"])

                profile = UserProfile.objects.get(user=user)
                if profile is None:
                    profile = UserProfile.objects.create(user=user)

                vendor = vendor_serializer.save(user=user, user_profile=profile)

            return Response({"success": True,"data": {
                    "user_id": user.id,
                    "email": user.email,
                    "vendor_id": vendor.id,
                    "vendor_name": vendor.vendor_name,
                    "is_approved": vendor.is_approved,
                },
                "error": None,
            },
            status=status.HTTP_201_CREATED,
        )
        
        else:
            return Response(
                {
                    "success": False,
                    "data": None,
                    "error": {
                        "user": user_serializer.errors if not user_serializer.is_valid() else {},
                        "vendor": vendor_serializer.errors if not vendor_serializer.is_valid() else {},
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        