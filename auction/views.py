import base64
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from .models import Users,Categories,Product,AuctionList,Bid
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection,IntegrityError
import smtplib
import smtplib
import threading
import time

from django.core.mail import send_mail
from django.core.mail import EmailMessage 
from online_auction.settings import EMAIL_HOST_USER
flag=0
userrid=0
from .models import Product
from datetime import datetime
from django.shortcuts import render
auct=AuctionList.objects.values()
table=[]
def index(request):
    print(table)
    auct=AuctionList.objects.values()
    for a in auct:
         send=a['end']
         send = send.strftime("%Y-%m-%d %H:%M:%S")
         ad=a['auc_id']
         if ad in table:
            continue
         else:
            pd=a['product_id']
            pp=Product.objects.filter(prod_id=pd)
            if pp:
              x=send_email1(send,ad,pp[0].seller_id)
              y=send_email2(send,ad,pp[0].seller_id)
              if(x==True and y==True):
                   table.append(ad)
    prods = Product.objects.values('prod_id', 'prod_name', 'image')
    products1=[]
    products2=[]
    for p in prods:
         a=AuctionList.objects.filter(product_id=p['prod_id'])
         print(a)
         current_time = datetime.now()
         current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
         if a:
            end = a[0].end.strftime("%Y-%m-%d %H:%M:%S")
            start = a[0].start.strftime("%Y-%m-%d %H:%M:%S")
            if(start<=current_time and current_time<=end):
                
                products1.append(p)
            elif(start>current_time):
             
              products2.append(p)
    data1 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products1]
    data2 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products2]
   
    
    return render(request, 'index.html', {'data1': data1,'data2':data2})
def user(request):
	return render(request,'user.html')
def signup(request):
	return render(request,'signup.html')
def userdata(request):
    if request.method == 'POST':
        name = request.POST['fullname']
        uname = request.POST['username']
        phone = request.POST['phone']
        mail = request.POST['email']
        strno = request.POST['strno']
        strname = request.POST['strname']
        state = request.POST['state']
        city = request.POST['city']
        zip = request.POST['zip']
        password = request.POST['pass']
        password1 = request.POST['pass1']
        
        if Users.objects.exists():
            row = Users.objects.latest('user_id')
            user_id = row.user_id+1
        else:
            user_id = 1
        
        try:
            user = Users(
                user_id=user_id,
                user_name=uname,
                name=name,
                gmail=mail,
                phone=phone,
                streetno=strno,
                streetname=strname,
                city=city,
                state=state,
                zipcode=zip,
                password=password
            )
            user.save()
            global userrid
            userrid=user_id
            
        except IntegrityError as e:
            error_message = str(e)
            return render(request, 'signup.html', {'error_message': error_message, 'data':request.POST})

        if(password!=password1):
            error_message = "password does not match"
            return render(request, 'signup.html', {'error_message': error_message,'data': request.POST})
        
    prods = Product.objects.values('prod_id', 'prod_name', 'image')
    products1=[]
    products2=[]
    for p in prods:
         a=AuctionList.objects.filter(product_id=p['prod_id'])
         print(a)
         current_time = datetime.now()
         current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
         if a:
            end = a[0].end.strftime("%Y-%m-%d %H:%M:%S")
            start = a[0].start.strftime("%Y-%m-%d %H:%M:%S")
            if(start<=current_time and current_time<=end):
                print("jj")
                products1.append(p)
            elif(start>current_time):
                print("kk")
                products2.append(p)
    data1 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products1]
    data2 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products2]
    print(data1,data2)
    return render(request, 'index.html', {'data1': data1,'data2':data2})

def login(request):
    global flag
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            row = Users.objects.get(user_name=username)
        except ObjectDoesNotExist:
            row=None
        if row and row.password==password:
            global userrid
            userrid=row.user_id
            print(userrid)
            print(flag)
            if flag==1:
                categories = Categories.objects.all()
                data = list(categories.values())  
                flag=0
                return render(request, 'sell.html', {'data': data})
                
            elif flag==2:
                prod = request.session.get('pid', None)
                rows = AuctionList.objects.filter(product_id=prod)
                row1 = Product.objects.get(prod_id=prod)
                s = Users.objects.filter(user_id=row1.seller_id)
                name=s[0].user_name
                flag=0
                try:
                    latest_bid = Bid.objects.filter(prod_id=prod).latest('bidding_id')
                    latest_price = latest_bid.bid_amount
                except ObjectDoesNotExist:
                    latest_price = row1.start_bid
                    
                date_string = str(rows[0].end)
                date_obj = datetime.fromisoformat(date_string)
                time = date_obj.strftime("%Y-%m-%dT%H:%M:%S")
                return render(request, 'bid.html', {'data': time,'data1':row1,'price':latest_price,'name':name})
            elif (flag==3):
                 flag=0
                 return render(request,'yourprod.html')
            else:     
                prods = Product.objects.values('prod_id', 'prod_name', 'image')
                products1=[]
                products2=[]
                for p in prods:
                    a=AuctionList.objects.filter(product_id=p['prod_id'])
                    print(a)
                    current_time = datetime.now()
                    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    if a:
                        end = a[0].end.strftime("%Y-%m-%d %H:%M:%S")
                        start = a[0].start.strftime("%Y-%m-%d %H:%M:%S")
                        if(start<=current_time and current_time<=end):
                            print("jj")
                            products1.append(p)
                        elif(start>current_time):
                            print("kk")
                            products2.append(p)
                data1 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products1]
                data2 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products2]
                print(data1,data2)
                return render(request, 'index.html', {'data1': data1,'data2':data2})
               
        else:
            error_message = "username or password wrong. try again"
            return render(request, 'user.html', {'error_message': error_message,'data': request.POST})

def sell(request):
     if userrid==0:
        global flag
        flag=1
        return render(request,'user.html')
     else:
        categories = Categories.objects.all()
        data = list(categories.values())
        print(data)  
        return render(request, 'sell.html', {'data': data})
def product(request):
    if request.method == 'POST':
        prod_name = request.POST.get('Prod_name')
        prod_desc = request.POST.get('Product_desc')
        start_bid = request.POST.get('Start_bid')
        min_bid = request.POST.get('Min_bid')
        seller_id = userrid
        cat_id = request.POST.get('Cat_id')
        print("aaaaakkkkkkk")
        start = request.POST.get('start')
        end = request.POST.get('end')
        if request.FILES.get('image'):
            image = request.FILES['image']
        else:
            image = None
        latest_product = Product.objects.order_by('-prod_id').first()
        if latest_product:
            prod_id = latest_product.prod_id + 1
        else:
            prod_id = 1

        # Retrieve the latest auc_id
        latest_auction = AuctionList.objects.order_by('-auc_id').first()
        if latest_auction:
            auc_id = latest_auction.auc_id + 1
        else:
            auc_id = 1
        print(userrid,cat_id)
        new_product = Product(
            prod_id=prod_id,
            prod_name=prod_name,
            prod_desc=prod_desc,
            start_bid=start_bid,
            min_bid=min_bid,
            seller_id=userrid,
            cat_id=cat_id,
            image=image
        )
        
        new_product.save()
        new_auc=AuctionList(
            auc_id=auc_id,
            start=start,
            end=end,
            product_id=new_product.prod_id,
            winner_id=1,
            auc_payment=userrid
        )
        print(new_auc)
        new_auc.save()
        prods = Product.objects.values('prod_id', 'prod_name', 'image')
        products1=[]
        products2=[]
        for p in prods:
            a=AuctionList.objects.filter(product_id=p['prod_id'])
            print(a)
            current_time = datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            if a:
                end = a[0].end.strftime("%Y-%m-%d %H:%M:%S")
                start = a[0].start.strftime("%Y-%m-%d %H:%M:%S")
                if(start<=current_time and current_time<=end):
                    print("jj")
                    products1.append(p)
                elif(start>current_time):
                    print("kk")
                    products2.append(p)
        data1 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products1]
        data2 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products2]
        print(data1,data2)      
        return render(request, 'index.html', {'data1': data1,'data2':data2})
        
        
def bid(request):
     prod = request.POST['pid']
     request.session['pid'] = prod
     if userrid==0:
        global flag
        flag=2
        return render(request,'user.html')
     else:
        
        rows = AuctionList.objects.filter(product_id=prod)
        row1 = Product.objects.get(prod_id=prod)
        s = Users.objects.filter(user_id=row1.seller_id)
        name=s[0].user_name
        try:
            latest_bid = Bid.objects.filter(prod_id=prod).latest('bidding_id')
            latest_price = latest_bid.bid_amount
        except ObjectDoesNotExist:
            latest_price = row1.start_bid
             
        date_string = str(rows[0].end)
        date_obj = datetime.fromisoformat(date_string)
        time = date_obj.strftime("%Y-%m-%dT%H:%M:%S")
        return render(request, 'bid.html', {'data': time,'data1':row1,'price':latest_price,'name':name})
def raisebid(request):
    prod = request.session.get('pid', None)
    row1 = Product.objects.get(prod_id=prod)
    try:
            latest_bid = Bid.objects.filter(prod_id=prod).latest('bidding_id')
            latest_price = latest_bid.bid_amount
    except ObjectDoesNotExist:
            latest_price = row1.start_bid
    return render(request,'setauction.html',{'maxbid':latest_price,'inter':row1.min_bid})
def bidd(request):
    bid1=request.POST['bidam']
    print(bid1)
    prod = request.session.get('pid', None)
    if Bid.objects.exists():
            row = Bid.objects.latest('bidding_id')
            bidding_id = row.user_id+1
    else:
            bidding_id = 1
    new_auc=Bid(
            bidding_id = bidding_id,
            user_id = userrid,
            bid_amount =bid1,
            prod_id = prod
        )
    new_auc.save()
    prods = Product.objects.values('prod_id', 'prod_name', 'image')
    products1=[]
    products2=[]
    for p in prods:
         a=AuctionList.objects.filter(product_id=p['prod_id'])
         print(a)
         current_time = datetime.now()
         current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
         if a:
            end = a[0].end.strftime("%Y-%m-%d %H:%M:%S")
            start = a[0].start.strftime("%Y-%m-%d %H:%M:%S")
            if(start<=current_time and current_time<=end):
                print("jj")
                products1.append(p)
            elif(start>current_time):
                print("kk")
                products2.append(p)
    data1 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products1]
    data2 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products2]
    print(data1,data2)
    return render(request, 'index.html', {'data1': data1,'data2':data2})
def bidprod(request):
    prods = Product.objects.values('prod_id', 'prod_name', 'image')
    products1=[]
    for p in prods:
         a=AuctionList.objects.filter(product_id=p['prod_id'])
         print(a)
         if a:
            current_time = datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            end = a[0].end.strftime("%Y-%m-%d %H:%M:%S")
            start = a[0].start.strftime("%Y-%m-%d %H:%M:%S")
            if(start<=current_time and current_time<=end):
                print("jj")
                products1.append(p)
    data1 = [{'id': product['prod_id'], 'image': product['image'], 'name': product['prod_name']} for product in products1]
    return render(request, 'bidprod.html', {'data': data1})
def yourprod(request):
     if userrid==0:
        global flag
        flag=3
        return render(request,'user.html')
     else:
        return render(request,'yourprod.html')
def bidding(request):
    prod_ids = Bid.objects.filter(user_id=userrid).values_list('prod_id', flat=True)
    products = Product.objects.filter(prod_id__in=prod_ids)
    data = [{'id': product.prod_id, 'image': product.image, 'name': product.prod_name} for product in products]
    return render(request, 'bidding.html', {'data': data})
def info1(request):
        
        prod = request.POST['pid']
        rows = AuctionList.objects.filter(product_id=prod)
        row1 = Product.objects.get(prod_id=prod)
        s = Users.objects.filter(user_id=row1.seller_id)
        name=s[0].user_name
        try:
            latest_bid = Bid.objects.filter(prod_id=prod).latest('bidding_id')
            latest_price = latest_bid.bid_amount
        except ObjectDoesNotExist:
            latest_price = row1.start_bid
        winner=rows[0].winner_id
        x=False
        
        current_time = datetime.now()
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        dt = rows[0].end.strftime("%Y-%m-%d %H:%M:%S")
        if(winner==userrid and dt<current_time):
             x=True
        date_string = str(rows[0].end)
        date_obj = datetime.fromisoformat(date_string)
        time = date_obj.strftime("%Y-%m-%dT%H:%M:%S")
        return render(request, 'info1.html', {'data': time,'data1':row1,'price':latest_price,'name':name,'winner':x})
def prod(request):
    products = Product.objects.filter(seller_id=userrid)
    data = [{'id': product.prod_id, 'image': product.image, 'name': product.prod_name} for product in products]
    return render(request, 'prod.html', {'data': data})
def info2(request):
        prod = request.POST['pid']
        rows = AuctionList.objects.filter(product_id=prod)
        row1 = Product.objects.get(prod_id=prod)
        s = Users.objects.filter(user_id=row1.seller_id)
        name=s[0].user_name
        try:
            latest_bid = Bid.objects.filter(prod_id=prod).latest('bidding_id')
            latest_price = latest_bid.bid_amount
        except ObjectDoesNotExist:
            latest_price = row1.start_bid
        date_string = str(rows[0].end)
        date_obj = datetime.fromisoformat(date_string)
        time = date_obj.strftime("%Y-%m-%dT%H:%M:%S")
        return render(request, 'info2.html', {'data': time,'data1':row1,'price':latest_price,'name':name})
def send_email1(send_time, auc_id,seller_id):
        print("HEREEEEE")
        u=Users.objects.get(user_id=seller_id)
        a=AuctionList.objects.get(auc_id=auc_id)
        p=Product.objects.get(prod_id=a.product_id)
        receiver_email=u.gmail
        product=p.prod_name
        amount=a.auc_payment
        u1=Users.objects.get(user_id=a.winner_id)
        person=u1.user_name
        email=u1.gmail
        phone=u1.phone
        current_time = datetime.now()
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        
        
        if(current_time>send_time):
                    print("wtfff")
                    body = f"HEYYY!!! AUCTION ENDED FOR YOUR PRODUCT {product}\nDETAILS OF THE WINNER: \nWINNER NAME: {person}\nCONTACT: {phone}\nMAIL: {email}\nAMOUNT YOU'LL RECEIVE FOR YOUR PRODUCT: {amount}\n"
                    to=[receiver_email]
                    send_mail(" AUCTION RESULT: ",body,EMAIL_HOST_USER,to,fail_silently=True)
                    return True
        return False
def send_email2(send_time, auc_id,seller_id):
        u=Users.objects.get(user_id=seller_id)
        a=AuctionList.objects.get(auc_id=auc_id)
        p=Product.objects.get(prod_id=a.product_id)
        email=u.gmail
        product=p.prod_name
        amount=a.auc_payment
        u1=Users.objects.get(user_id=a.winner_id)
        person=u.user_name
        phone=u.phone
        receiver_email=u1.gmail
        
        current_time = datetime.now()
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if(current_time>send_time):
            print("iamhere")
            body = f"CONGRATULATIONS!!! YOU WON THE AUCTION FOR THE PRODUCT {product}\nDETAILS OF THE SELLER:\nSELLER NAME: {person}\nSELLER CONTACT: {phone}\nSELLER MAIL: {email}\nAMOUNT TO PAY: {amount}\n"
            to=[receiver_email]
            send_mail(" AUCTION RESULT: ",body,EMAIL_HOST_USER,to,fail_silently=True)
            return True   
        return False    
            
