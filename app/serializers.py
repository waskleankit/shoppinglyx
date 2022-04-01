from .models import Customer,Product,Cart,OrderPlaced
from rest_framework import serializers

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user','name','locality',
                    'city','zipcode','state']

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','selling_price',
                    'discounted_price','description','brand','category',
                    'product_image']

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user','product','quantity']

class OrderPlacedSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderPlaced
        fields = ['user','customer','product',
                    'quantity','ordered_date','status']