from django.shortcuts import render,redirect
from  django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm ,\
 CustomerProfileForm
from django.contrib import messages

from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# from django.views.decorators.csrf import csrf_exempt



# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
 def get(self,request):
  totalitem = 0
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptop = Product.objects.filter(category='L')
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  context = {'topwears': topwears,'bottomwears' : bottomwears,'mobiles' : mobiles,'laptop': laptop,'totalitem':totalitem}
  return render(request,'app/home.html',context)

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
   item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  context = {'totalitem':totalitem,'product':product,'item_already_in_cart':item_already_in_cart}
  return render(request,'app/productdetail.html',context)

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  # print(cart)
  amount= 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  # print(cart_product)
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shipping_amount
   return render(request, 'app/addtocart.html',{'totalitem':totalitem,'carts':cart,'total_amount':total_amount,'amount' : amount})
  else:
   return render(request,'app/emptycart.html',{'totalitem' : totalitem})

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  # print(prod_id)
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
   totalamount = amount + shipping_amount

  data = {
  'quantity':c.quantity,
  'amount':amount,
  'totalamount':totalamount
   }
  return JsonResponse(data)

def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  # print(prod_id)
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
   totalamount = amount + shipping_amount

  data = {
  'quantity':c.quantity,
  'amount':amount,
  'totalamount':totalamount
   }
  return JsonResponse(data)


def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  # print(prod_id)
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
  data = {
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)




def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 context = {'add': add, 'active': 'btn-primary', 'totalitem': totalitem}
 return render(request, 'app/address.html',context)



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
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request,data = None):
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data=='Apple' or data =='Dell' or data =='Hp' or data =='Lg':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt = 10000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt = 10000)
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})

def topwear(request,data = None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data=='brandname4' or data =='brandname3' or data =='brandname' or data =='brandname6' or data =='brandname5' or data =='brandname1':
  topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__lt = 10000)
 elif data == 'above':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__gt = 10000)
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/topwear.html',{'topwears':topwears,'totalitem':totalitem})

def bottomwear(request,data = None):
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data=='Lee' or data =='Levis' or data =='BlueBuddha' or data =='brandname3' or data =='banrandname4' or data =='brandname5':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt = 10000)
 elif data == 'above':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt = 10000)
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears,'totalitem':totalitem})


# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
# @csrf_exempt
class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  context = {'form':form}
  return render(request,'app/customerregistration.html',context)
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations!! Registered Successfully')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   # print(tempamount)
   amount += tempamount
   # print(amount)
  totalamount = amount + shipping_amount
  # print(totalamount)
 # totalitem = 0
 # if request.user.is_authenticated:
 #  totalitem = len(Cart.objects.filter(user=request.user))
 # context = {'totalitem':totalitem,'add':add,'totalamount':totalamount,'cart_items':cart_items}
 context = {'add':add,'totalamount':totalamount,'cart_items':cart_items}
 return render(request, 'app/checkout.html',context)

@login_required
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart :
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect("orders")

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 totalitem = 0
 if request.user.is_authenticated:
  totalitem = len(Cart.objects.filter(user=request.user))
 context = {'order_placed':op,'totalitem':totalitem}
 return render(request, 'app/orders.html',context)

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
   # prev_customer = [p for p in Customer.objects.all() if p.user == request.user]
   # if prev_customer:
   #  return render(request,'app/home.html')
   prev_customer =len(Customer.objects.filter(user=request.user))
   print(prev_customer)
   if (prev_customer >= 1):
    return redirect("home")
  return render(request,'app/profile.html',{'totalitem':totalitem,'form':form,'active':'btn-primary'})

 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality= form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congradulations!! Profile Updated Successfully')
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return redirect("home")

