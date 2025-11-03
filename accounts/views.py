from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import io
from .models import User
from rest_framework import status
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





