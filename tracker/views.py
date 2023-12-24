from rest_framework.views import APIView
from .serializer import LoginSerilizer,RegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistrationView(APIView):
    def post(self, request, format= None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception= True):
            user  = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,"msg":"User Registred"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request,format= None):
        serializer = LoginSerilizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,"msg":"User Logged in"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors":{'non_fieled_errors':['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        return Response({'msg':f" welcome {request.user}"},status=status.HTTP_200_OK)
    