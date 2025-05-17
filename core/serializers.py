from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import UserProfile, Company
from rest_framework import serializers
from .models import User


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'industry', 'number_of_employees']

class AdminRegisterSerializer(serializers.ModelSerializer):
    # Profile fields
    company = CompanySerializer(write_only=True)
    phone_number = serializers.CharField(required=True, write_only=True)
    country = serializers.CharField(required=True, write_only=True)
    city = serializers.CharField(required=True, write_only=True)
    state = serializers.CharField(required=True, write_only=True)
    
    # User fields
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password2',
            'company', 'phone_number', 'country', 'city', 'state'
        ]
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        # Extract nested data
        company_data = validated_data.pop('company')
        password = validated_data.pop('password')
        validated_data.pop('password2')
        
        # Extract profile fields
        profile_data = {
            'phone_number': validated_data.pop('phone_number'),
            'country': validated_data.pop('country'),
            'city': validated_data.pop('city'),
            'state': validated_data.pop('state'),
            'user_type': 'admin',  # Set default user_type for admin registration
        }
        
        # Create company
        company = Company.objects.create(**company_data)
        
        # Create user
        user = User.objects.create_user(
            **validated_data,
            password=password
        )
        
        # Update the automatically created profile with our data
        user_profile = UserProfile.objects.get(user=user)
        for key, value in profile_data.items():
            setattr(user_profile, key, value)
        
        # Assign company to profile
        user_profile.company = company
        user_profile.save()
        
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
