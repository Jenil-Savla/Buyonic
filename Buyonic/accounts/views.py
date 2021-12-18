from django.contrib.auth import authenticate,login

from .models import MyUser
from .serializers import RegisterSerializer, LoginSerializer

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.response import Response

class RegisterAPI(GenericAPIView):
    
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]
	
    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
		
        return Response(serializer.data
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
			return Response({'token' : token.key,'username' : user.username},status = status.HTTP_200_OK)
		return Response('Invalid Credentials',status = status.HTTP_404_NOT_FOUND)

class LogoutAPI(GenericAPIView):

    queryset = MyUser.objects.all()

    def get(self,request,format=None):
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)

