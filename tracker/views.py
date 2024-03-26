from rest_framework.views import APIView
from .serializer import LoginSerilizer, RegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import Product, PriceHistory,CustomUser
from datetime import datetime, timedelta
from django.db.models import F, Max
from django.db.models import F,Max
from django.core.mail import send_mail
from django.utils.html import strip_tags
import logging
from django.conf import settings

# Create your views here.
# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, "msg": "User Registered"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerilizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, "msg": "User Logged in"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {'non_field_errors': ['Email or password is not valid']}},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UrlDesiredView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        url = body['url']
        desired_price = body['desired_price']
        data = Product(user=user, url=url, desired_price=desired_price)
        data.save()
        return HttpResponse("url added")

    def get(self, request):
        user = request.user
        data = Product.objects.filter(user=user).values('url', 'desired_price')
        data_list = list(data)
        return JsonResponse(data_list, safe=False)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'msg': f" welcome {request.user}"}, status=status.HTTP_200_OK)


class Ayearprice(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        from datetime import datetime, timedelta

        current_date = datetime.now()
        one_year_ago = current_date - timedelta(days=365)

        user_products = Product.objects.filter(user=user)
        price_histories = []
        for product in user_products:
            product_price_histories = PriceHistory.objects.filter(product=product,product_id=id,created_date__gte=one_year_ago).all()
            for price in product_price_histories: 
                prices = price.last_price
                price_histories.append(prices)
        print(price_histories)
        return HttpResponse("nothing much")

class UserDashboardView(APIView):
    ''' 
    return url for specific users
    '''
    def get(self, request):
        '''
        from product details to product
        '''
        # product_details = ProductDetail.objects.all().select_related('product')
        # datas =[]
        # for product in product_details:
        #     data ={
        #         'product':product.name,
        #         "desired Price":product.product.desired_price
        #     }
        #     datas.append(data)
        # print(datas)

        '''
        from product to product details
        '''
        user = request.user
        # products = Product.objects.filter(user=user).all().prefetch_related("productdetail_set","pricehistory_set")
        # for product in products:
        #     price_history =product.pricehistory_set.all()
        #     for detail in price_history:
        #         print(detail.last_price)

        # products = Product.objects.filter(user=user).all()
        products = Product.objects.filter(user=user).all().prefetch_related("pricehistory_set")
        data=[]

        for product in products:
            product_dict = {
                "desired_price":product.desired_price
            }
            price_history = product.pricehistory_set.order_by('-created_date').first()
            try:
                product_dict['last_price']=price_history.last_price
            except:
                product_dict['last_price']="yet to scrape"

            detail = product.productdetail_set.first()
            try:
                product_dict['name']=detail.name
            except:
                product_dict['name']='yet to scrape'

            data.append(product_dict)
        
        print(data)

        return HttpResponse('no more')
