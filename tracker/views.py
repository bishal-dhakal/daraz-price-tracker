from rest_framework.views import APIView
from .serializer import LoginSerilizer,RegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from tracker.scrape import scrape_data
from django.http import JsonResponse
import json
from .models import Product, ProductDetail, PriceHistory
from rest_framework import serializers

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
    

class ScrapeView(APIView):
    def get(self,request,format=None):
        """
        logic to store price data in db using function in scrape.py
        """
        try:
            urls = Product.objects.all()
        except:
            return "No Url Found"
        
        # TODO : store it in database 
        for  product in urls:
            url = product.url
            id = product.id
        
            title,price, description = scrape_data(url)
            product_details = ProductDetail.objects.filter(product_id=id)
            if product_details is None:
                detail = ProductDetail(product_id=id,name = title, description= description)
                detail.save()
            detail2 = PriceHistory(product_id=id,last_price=price)
            detail2.save()
        return  HttpResponse(f'scraping Completed',status=status.HTTP_200_OK)
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,format=None):
        user = request.user
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        url = body['url']
        desired_price= body['desired_price']
        data = Product(user=user,url=url,desired_price=desired_price)
        data.save()
        return HttpResponse("url added")
    
    def get(self,request,format=None):
        user = request.user
        data = Product.objects.filter(user=user).values('url','desired_price')
        data_list = list(data)
        print(data)
        return JsonResponse(data_list,safe=False)

