from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from core.serializers import AdminRegisterSerializer
from rest_framework.permissions import AllowAny
from core.serializers import AdminRegisterSerializer

from core.models import UserProfile
from core.serializers import UserSerializer
from core.permissions import IsAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"status": "user activated"})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"status": "user deactivated"})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AdminRegisterSerializer

class AdminRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminRegisterSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Manually construct response data to avoid serialization issues
        profile = user.profile
        
        # Build response data
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        
        profile_data = {
            'phone_number': profile.phone_number,
            'country': profile.country,
            'city': profile.city,
            'state': profile.state,
            'user_type': profile.user_type
        }
        
        company_data = CompanySerializer(profile.company).data if profile.company else None
        
        return Response({
            'user': user_data,
            'profile': profile_data,
            'company': company_data,
            'message': 'Admin user created successfully'
        }, status=status.HTTP_201_CREATED)