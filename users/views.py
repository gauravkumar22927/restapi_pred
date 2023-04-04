from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes ,authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from .authentication import generate_access_token ,JWTAuthentication
from .models import User
from .serializers import UserSerializer
# Create your views here.

@api_view(['POST'])
def register(request):
  data = request.data

  if data['password'] != data['password_confirm']:
    raise exceptions.APIException('passwords do not match!')

  serializer = UserSerializer(data = data)
  serializer.is_valid(raise_exception = True)
  serializer.save()
  return Response(serializer.data)


@api_view(['POST'])
def login(request):
  email = request.data.get('email')
  password = request.data.get('password')
  user = User.objects.filter(email=email).first()
  if user is None:
    raise exceptions.AuthenticationFailed("User not found!")

  if not user.check_password(password):
    raise exceptions.AuthenticationFailed('Incorrect Password!')
  
  response = Response()
  token = generate_access_token(user)

  response.set_cookie(key = 'jwt' , value = token,httponly = True)
  response.data = {
    'jwt' : token
  }
  return response

class AuthenticatedUser(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  def get(self,request):
    serializer = UserSerializer(request.user)

    return Response({
      'data' : serializer.data
    })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    price = request.data.get('price')
    mrp = request.data.get('mrp')
    content = {
        'status': 'request was permitted',
        'data' : price - mrp
    }
    return Response(content)

class PredictionClass(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  def post(self,request):
    price = request.data.get('price')
    mrp = request.data.get('mrp')

    return Response({
      'data' : price - mrp
    })

@api_view(['POST'])
def logout(_):
  response = Response()
  response.delete_cookie(key = 'jwt')
  response.data = {
    'message' : 'Success'
  }
  return response

@api_view(['POST'])
def users(request):
  serializer = UserSerializer(User.objects.all(),many = True)
  return Response(serializer.data)