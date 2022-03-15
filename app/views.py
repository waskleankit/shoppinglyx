from django.shortcuts import render
from  django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages
# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
 def get(self,request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptop = Product.objects.filter(category='L')
  return render(request,'app/home.html',
                {'topwears': topwears,
                 'bottomwears' : bottomwears,
                 'mobiles' : mobiles,
                 'laptop': laptop })

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  return render(request,'app/productdetail.html',
                {'product':product})

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data = None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data=='Redmi' or data =='Samsung' or data =='Apple' or data =='Sony':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt = 10000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt = 10000)
 return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request,data = None):
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data=='Apple' or data =='Dell' or data =='Hp' or data =='Lg':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt = 10000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt = 10000)
 return render(request, 'app/laptop.html',{'laptops':laptops})

def topwear(request,data = None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data=='brandname4' or data =='brandname3' or data =='brandname' or data =='brandname6' or data =='brandname5' or data =='brandname1':
  topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__lt = 10000)
 elif data == 'above':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__gt = 10000)
 return render(request, 'app/topwear.html',{'topwears':topwears})

def bottomwear(request,data = None):
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data=='Lee' or data =='Levis' or data =='BlueBuddha' or data =='brandname3' or data =='banrandname4' or data =='brandname5':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt = 10000)
 elif data == 'above':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt = 10000)
 return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})


def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations!! Registered Successfully')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})

def checkout(request):
 return render(request, 'app/checkout.html')
