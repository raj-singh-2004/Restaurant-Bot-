from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from rest_framework import serializers
from .models import User
from vendor.models import Vendor

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "username", "email", "phone_number",
            "role", "password", "confirm_password"
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "username": {"required": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        pwd = attrs.get("password")
        confirm = attrs.pop("confirm_password", None)
        if pwd != confirm:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        try:
            with transaction.atomic():
                user = User(**validated_data)
                user.set_password(password)      
                user.is_active = False            
                user.is_staff = False             
                user.save()
                return user
        except IntegrityError:
            # Handles rare race conditions on unique fields
            raise serializers.ValidationError({"email": "This email is already registered."})

class VendorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_license"] 
        extra_kwargs = {"vendor_name": {"required": True}, "vendor_license": {"required": True}}

    def create(self, validated_data):
        # DRF merges kwargs passed to .save() into validated_data
        user = validated_data.pop("user")
        user_profile = validated_data.pop("user_profile")
        return Vendor.objects.create(user=user, user_profile=user_profile, **validated_data)
