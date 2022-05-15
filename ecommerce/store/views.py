from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import *
from .forms import *
from .utils import cookieCart, cartData, guestOrder
from django.http import HttpResponseRedirect, Http404
from math import ceil


# Create your views here.
def store(request):
    
    
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    category = Category.objects.all()
    frontend= FrontEndSettings.objects.values_list('navbarcolor')
    
    

    sitelogo = SiteImage.objects.all().order_by('-id')[:1]
    site_name = SiteName.objects.all().order_by('-id')[:1]
    context = {'frontend':frontend,'category':category,'items' :items,'order':order, 'products' :products, 'cartItems' :cartItems,'site_name':site_name, 'sitelogo': sitelogo,}
    return render(request, 'store/store.html', context)






def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    sitelogo = SiteImage.objects.all().order_by('-id')[:1]
    site_name = SiteName.objects.all().order_by('-id')[:1]
    context = {'items' :items, 'order' :order, 'cartItems':cartItems,'site_name':site_name, 'sitelogo': sitelogo}
    return render(request, 'store/cart.html', context)




def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    sitelogo = SiteImage.objects.all().order_by('-id')[:1]
    site_name = SiteName.objects.all().order_by('-id')[:1]
    context = {'items' :items, 'order' :order, 'cartItems':cartItems,'site_name':site_name, 'sitelogo': sitelogo}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print(orderItem)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)


    else:
        customer, order = guestOrder(request,data )
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)


def logout_page(request):
    sitelogo = SiteImage.objects.all().order_by('-id')[:1]
    site_name =  SiteName.objects.all().order_by('-id')[:1]
    context={'site_name':site_name, 'sitelogo': sitelogo}
    return render(request, 'store/logout_page.html',context)



def settings(request):
    site_name = SiteName.objects.all().order_by('-id')[:1]
    
    update_Form = updateForm()
    if request.method == 'POST':
        update_Form = updateForm(request.POST, request.FILES)
        if update_Form.is_valid():
            update_Form.save()


    
    update_Form_image = updateFormImage()
    if request.method == 'POST':
        update_Form_image = updateFormImage(request.POST, request.FILES)
        if update_Form_image.is_valid():
            update_Form_image.save()
            return HttpResponseRedirect('/settings')
    context={'update_Form':update_Form,
             'update_Form_image':update_Form_image,'site_name':site_name}
    return render(request, 'store/settings.html', context)








def navbar(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    productcategory = ProductCategory.objects.all()
    sitelogo = SiteImage.objects.all().order_by('-id')[:1]
    site_name = SiteName.objects.all().order_by('-id')[:1]
    context = {'productcategory':productcategory,'items' :items, 'order' :order, 'cartItems':cartItems,'site_name':site_name, 'sitelogo': sitelogo}
    return render(request, 'store/store_navbar.html', context)

def tabname(request):
  
    site_name = SiteName.objects.all().order_by('-id')[:1]
    context={'site_name':site_name}
    return render(request, 'store/bootstrap_primary.html', context)



def product_view(request, pk_test):
    
    details = Product.objects.get(id=pk_test)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    sitelogo = SiteImage.objects.all().order_by('-id')[:1]

    sp = details.price
    dis = details.strike_out_price
    
    if dis == None:
        percent = 0

    else:
        percent = 100-(sp*100)/dis
        if percent>100:
            percent = 0
        elif percent<0:
            percent = 0
        
    

    context={'items' :items, 'order' :order, 'cartItems':cartItems, 'sitelogo': sitelogo, 'details':details, 'percent':percent}
    return render(request, 'store/view_product.html', context)



def product_category(request, cats):
    productcategory = Product.objects.filter(category=cats)
    category = Category.objects.all()
    site_name =  SiteName.objects.all().order_by('-id')[:1]

    context={'category':category,'productcategory':productcategory, 'cats':cats}
    return render(request, 'store/store_extend.html', context )


def add_products(request):
    category = Category.objects.all()
    products = Product.objects.all()
    form = addProductForm()
    product_count = Product.objects.count  
    site_name = SiteName.objects.all().order_by('-id')[:1]
    if request.method == 'POST':
        form = addProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_product')

    category_form = addCategoryForm()
    if request.method == 'POST':
        #print(request.POST)
        form = addCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_product') 
       
 
    context = {'site_name':site_name, 'product_count':product_count, 'products':products, 'category':category, 'form':form,'category_form':category_form }
    return render(request, 'store/add_products.html', context)


def dashboard(request):
    product_count = Product.objects.count
    site_name = SiteName.objects.all().order_by('-id')[:1]

    
    
    context={'site_name':site_name, 'product_count':product_count}
    return render(request, 'store/dashboard.html', context)


def dashboard_product_view(request):
    content=Product.objects.all()
    product_count = Product.objects.count
    site_name = SiteName.objects.all().order_by('-id')[:1]
    context={'site_name':site_name, 'product_count':product_count, 'content':content}
    return render(request, 'store/dashboard_products.html', context)



def edit(request,edit_products):

    details = Product.objects.get(id=edit_products)
    data_to_edit= get_object_or_404(Product, id=edit_products)
    form= addProductForm(instance=data_to_edit )
    product_count = Product.objects.count  

    if request.method == "POST":
        form= addProductForm(request.POST,instance=data_to_edit)
        if form.is_valid():
            data_to_edit=form.save(commit=False)
            data_to_edit.save()
            return HttpResponseRedirect('/product_dashboard')        
        else:
            form = addProductForm(instance=data_to_edit)
            return HttpResponseRedirect('/product_dashboard') 
            

    
    
    context={'form':form, 'product_count':product_count, 'details':details}
    return render(request, 'store/edit.html', context)


def delete(request, delete_products):
    
    product_to_delete = get_object_or_404(Product, id=delete_products)
    product_to_delete.delete()
    
    return HttpResponseRedirect('/product_dashboard') 

def delete_cat(request, delete_category):
    
    category_to_delete = get_object_or_404(Category, id=delete_category)
    category_to_delete.delete()
    return HttpResponseRedirect('/add_product') 
    


def login(request):
    
     context = {}
     return render(request, 'store/login.html', context) 
