from django.db.models import fields
from rest_framework import serializers
from .models import *
from .threads import *

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
)
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, label='Confirm password'
    )
    class Meta:
        model= CustomUser
        fields = ['email', 'name', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data['name']
        phone= validated_data['phone']
        password = validated_data['password']
        password2 = validated_data['password2']
        if (email and CustomUser.objects.filter(email=email).exists()):

            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'The two passwords differ.'})
        tok = str(uuid.uuid4())
        user = CustomUser(name=name, phone=phone, email=email,verification_token=tok)
        thread_obj = send_verification_email(email, tok)
        thread_obj.start()
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
         required=True )
