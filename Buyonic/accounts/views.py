from django.contrib.auth import authenticate,login

from .models import OTP, MyUser
from .serializers import OTPSerializer, RegisterSerializer, LoginSerializer,UserSerializer

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status,mixins
from rest_framework.authtoken.models import Token

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.response import Response

from twilio.rest import Client
from django.conf import settings
import random

def send_text(request,number,otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN )
    message = client.messages.create(body= f'Your OTP for buyonic is {otp}',
        to ='+91'+str(number),
        from_ ='+12346574691')
    return('success')

def send_email(data):
		email = EmailMessage(subject = data['subject'], body = data['email_body'], to = [data['to']])
		email.send()

class RegisterAPI(GenericAPIView):
    
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]
	
    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
		
        token = Token.objects.create(user=user)
        
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        link = 'http://'+current_site+relative_link+'?token='+ token.key
        data = {'email_body': f'Use this link to get verified {link}. If you are a manufacturer then please mail us. We will contact you regarding same.', 'subject':'Email Verification', 'to' : user.email}
        send_email(data)

        return Response({'token' : token.key}
		,status=status.HTTP_201_CREATED)


class LoginAPI(GenericAPIView):
	
	serializer_class = LoginSerializer
	
	def post(self,request,*args,**kwargs ):
		email = request.data.get('email',None)
		password = request.data.get('password',None)
		user = authenticate(email = email, password = password)
		if user :
			serializer = self.serializer_class(user)
			token,k = Token.objects.get_or_create(user=user)
			return Response({'token' : token.key},status = status.HTTP_200_OK)
		return Response('Invalid Credentials',status = status.HTTP_404_NOT_FOUND)

class OTPView(GenericAPIView):

    serializer_class = OTPSerializer
    permission_classes = [IsAuthenticated,]
    queryset = OTP.objects.all()

    def get(self,request):
        user = request.user
        one = random.randint(100000,999999)
        otp = OTP.objects.create(otp = one,user = user)
        serializer = self.serializer_class(instance=otp)
        k = send_text(request,user.contact,one)
        return Response('sent')

    def post(self,request):
        data = request.data
        user = request.user
        passw = OTP.objects.get(user=user)
        print(passw.otp)
        if data['otp'] == str(passw.otp):
            passw.delete()
            return Response({'success':'success'})
        else:
            passw.delete()
            return Response({'failure':'failure'})

class LogoutAPI(GenericAPIView):

    permission_classes = [IsAuthenticated,]

    queryset = MyUser.objects.all()

    def get(self,request,format=None):
        request.user.auth_token.delete()
        return Response({'logout':'logout successful'},status = status.HTTP_200_OK)

class EmailVerify(GenericAPIView):
    def get(self,request):
        token = request.GET.get('token')
        user = MyUser.objects.filter(auth_token = token).first()
        user.is_verified = True
        user.save()
        return Response('Account Verified', status=status.HTTP_200_OK)
    
class Waiting(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        return Response({'verified':request.user.is_verified})

class Profile(GenericAPIView):

    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    queryset = MyUser.objects.all()

    def get(self,request):
        user = request.user
        serializer = self.serializer_class(instance=user)
        return Response(serializer.data)

    def put(self,request):
        user = request.user
        data = request.data
        serializer = self.serializer_class(instance = user, context = {'request' : request},data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
