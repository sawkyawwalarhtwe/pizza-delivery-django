from django.shortcuts import get_object_or_404, render
from rest_framework import generics,status
from rest_framework.response import Response
from . import serializers
from .models import Order
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

User = get_user_model()
class HelloOrderView(generics.GenericAPIView):

    def get(self,request):
        return Response(data={"message":"Hello Order"}, status=status.HTTP_200_OK)


class OrderCreateListView(generics.GenericAPIView):
    
    serializer_class=serializers.OrderCreationSerializer
    queryset = Order.objects.all()
    permission_classes=[IsAdminUser]
    @swagger_auto_schema(operation_summary="List all order")
    def get(self,request):
        orders=Order.objects.all()
        serializer = self.serializer_class(instance=orders,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(operation_summary="create a new order")
    def post(self,request):

        data = request.data

        serializer=self.serializer_class(data=data)
        user=request.user

        if serializer.is_valid():
            serializer.save(customer=user)

            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
            
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

 
class OrderDetailsView(generics.GenericAPIView):
    permission_classes=[IsAdminUser]
    serializer_class=serializers.OrderDetailsSerializer
    @swagger_auto_schema(operation_summary="retrieve an order by order id")
    def get(self,request,order_id):
        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data,status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="update an order")
    def put(self,request,order_id):
        data=request.data

        order = get_object_or_404(Order, pk=order_id)
        serializer=self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data,status=status.HTTP_200_OK)

        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="delete an order")
    def delete(self,request,order_id):
        order = get_object_or_404(Order, pk=order_id)

        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateOrderStatus(generics.GenericAPIView):
    permission_classes=[IsAdminUser]
    serializer_class=serializers.OrderUpdateStatusSerializer
    @swagger_auto_schema(operation_summary="update an order status")
    def put(self,request,order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer=self.serializer_class(data=request.data,instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data,status=status.HTTP_200_OK)

        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class UserOrderView(generics.GenericAPIView):
    serializer_class=serializers.OrderDetailsSerializer
    @swagger_auto_schema(operation_summary="retrieve an order by user id")
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)

        order=Order.objects.all().filter(customer=user)
        serializer=self.serializer_class(instance=order,many=True)

    
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class UserOrderDetail(generics.GenericAPIView):
    serializer_class=serializers.OrderDetailsSerializer
    @swagger_auto_schema(operation_summary="retrieve an order by user and order ids")
    def get(self,request,order_id,user_id):
        user=User.objects.get(pk=user_id)

        order=Order.objects.all().filter(customer=user).get(pk=order_id)

        serializer=self.serializer_class(instance=order)

        return Response(data=serializer.data,status=status.HTTP_200_OK)