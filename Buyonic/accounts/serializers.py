from rest_framework import serializers

from .models import MyUser

import re

email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class RegisterSerializer(serializers.ModelSerializer):
	password=serializers.CharField(max_length=32,min_length=8,write_only = True)
	
	class Meta:
		model = MyUser
		fields = ['email','password','name','contact','address','city','state']
		
	def validate(self,attrs):
		email = attrs.get('email',' ')
		if not email_pattern.match(email):
			raise serializers.ValidationError('Email Address is invalid')
		return attrs
		
	def create(self,validated_data):
		return MyUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
	password=serializers.CharField(max_length=32,min_length=8,write_only = True)
	
	class Meta:
		model = MyUser
		fields = ['email','password']

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = MyUser
		fields = ['email','name','contact','address','city','state','refund_balance','is_verified']

	def validate_email(self, attrs):
		user = self.context['request'].user
		if MyUser.objects.exclude(pk=user.pk).filter(email=attrs).exists():
			raise serializers.ValidationError({'email':'This email already exists.'})
		return attrs

	def validate_contact(self, attrs):
		user = self.context['request'].user
		if MyUser.objects.exclude(email = user.email).filter(contact=attrs).exists():
			raise serializers.ValidationError({'contact':'This number already exists.'})
		return attrs

	def update(self,instance,validated_data):
		instance.email = validated_data['email']
		instance.name = validated_data['name']
		instance.contact = validated_data['contact']
		instance.address = validated_data['address']
		instance.city = validated_data['city']
		instance.city = validated_data['state']
		instance.refund_balance = validated_data['refund_balance']
		instance.save()
		return instance