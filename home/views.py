from home.models import CustomUser
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import request, viewsets
from .models import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from .models import *
from .threads import *


class RegisterViewSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class = RegisterSerializer

    @action(detail=True, methods=['post'])
    def login(self, request, pk=None):
        try:
            data = request.data
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                password=serializer.validated_data['password']
                user_obj = CustomUser.objects.filter(email=email).first()
                if user_obj is None:
                    return Response({"status": 400, "result": "Account does not exist"})
                if not user_obj.is_verified:
                    return Response({"status": 400, "result": "Email not verified. Check your mail"})
                user = authenticate(email=email, password=password)
                print(user)
                jwt_token = RefreshToken.for_user(user)
                return Response({
                    "status": 200, 
                    "result": "Login successfull", 
                    "token": str(jwt_token.access_token)
                    })
            return Response({"status": 400, "error": serializer.errors})
        except Exception as e:
            print(e)
        return Response({"status": 500, "message": "something went wrong"})
    
    @action(detail=True,methods=['get'])
    def verify(self, request, pk ):
        try:
            user = CustomUser.objects.get(verification_token=pk)
            if user.is_verified:
             return Response({"status": 400, "result": "Account is already verified"})
            user.is_verified = True
            user.save()
            return Response({
                    "status": 200, 
                    "result": "Account verification successfull"
                    })
        except Exception as e:
            print(e)
        return Response({"status": 500, "message": "something went wrong"})


                
