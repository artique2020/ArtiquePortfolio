from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError, connection, transaction
from django.contrib.auth import login,logout,authenticate
from django.db.models import Sum
from django.template.loader import render_to_string
from .models import Products, Product_Type, Transact_hdr, Transact_dtl, Appointment,subscriber
from .forms import AppointForm, SubscribeForm
from decimal import Decimal
from django.core.mail import send_mail
from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.contrib.admin.views.decorators import staff_member_required
from datetime import date

def signupuser(request):

    if request.method == 'GET':
        return render(request,'Signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                if request.POST['email'] and request.POST['last_name']:
                    usr = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'])
                    usr.save()
                    login(request,usr)

                    
                    return redirect('artiquehome')    
                else:
                    return render(request,'Signupuser.html', { 'error': 'Please enter Email Id and Mobile No.'})
                
            except IntegrityError:
                return render(request,'Signupuser.html', {'form': UserCreationForm(), 'error': 'Username exists'})
        else:
            return render(request,'Signupuser.html', {'form': UserCreationForm(), 'error': 'Password doesnt match'})

def artiquehome(request):
    prdtyp = Product_Type.objects.all()
    prod = Products.objects.filter(Display_main=True).order_by('-id')[:4]
    return render(request,'Bootstrap.html',{'prodtyp':prdtyp,'products': prod })

@login_required
def placeorder(request):
    return redirect('artiquehome')

@login_required
def myactivities(request):
    prdtyp = Product_Type.objects.all()
    Trans_hdr = Transact_hdr.objects.filter(user=request.user).order_by('-id')
    Trans = Transact_dtl.objects.filter(user=request.user).order_by('-id')
    Appnt = Appointment.objects.filter(user=request.user).order_by('-dt')
    return render(request,'myactivities.html', {'prodtyp':prdtyp,'CartH': Trans_hdr, 'Appnt': Appnt})

def ahome(request):
    
    prdtyp = Product_Type.objects.all()
    prod = Products.objects.filter(Display_main=True).order_by('-id')[:4]
    return render(request,'Home.html',{'prodtyp':prdtyp,'products': prod})

@staff_member_required
def OrderList(request):
    
    prdtyp = Product_Type.objects.all()
    Trans_hdr = Transact_hdr.objects.filter(~Q(Status = 'Pending')).order_by('-id')
    Appn = Appointment.objects.all().order_by('-dt')
    today =  date.today()
    return render(request,'OrderList.html',{'prodtyp':prdtyp,'Cart': Trans_hdr, 'Appn': Appn,'today': today})


def contactus(request):
    prdtyp = Product_Type.objects.all()
    if request.method == 'POST':
        form = SubscribeForm(request.POST)  
        form.save()
        return redirect('artiquehome')  
    else:
        return render(request,'ContactUs.html',{'prodtyp':prdtyp, 'form':SubscribeForm()})

def ourcollection(request,prd_pk):
    prdtyp = Product_Type.objects.all()
    prd = Products.objects.filter(Product_Type=prd_pk)
    return render(request,'Collections.html',{'products':prd , 'prodtyp':prdtyp})

def confirmsubscribe(request):    
    if request.method == 'POST':
        form = SubscribeForm(request.POST)  
        form.save()
        return redirect('artiquehome')        
    else:
        return redirect('artiquehome')        

@login_required
def appointment(request):
    prdtyp = Product_Type.objects.all()
    usr= request.user
    ap_name = usr.first_name
    ap_email = usr.email
    ap_mob = usr.last_name
    return render(request,'Appointment.html',{'prodtyp':prdtyp,'ap_name':ap_name,'ap_email':ap_email,'ap_mob':ap_mob, 'form':AppointForm() })
    
@login_required    
def confirmappoint(request):
    if request.method == 'POST':
        form = AppointForm(request.POST)  
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()

        subject = 'Your Appointment is confirmed...'
        
        usr= request.user
        ap_email = usr.email       

        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER,ap_email]

        #image_path = 'C:\Python\Artique\ArtiqueApp\static\images\Artique.jpg'
        image_path = settings.MEDIA_ROOT + '\ArtiqueApp\static\images\Artique.jpg'
        image_path1 = settings.MEDIA_ROOT + '\ArtiqueApp\static\images\Art_Attach.jpg'
        image_name = Path(image_path).name
        image_name1 = Path(image_path1).name
        
            
        msg_plain = render_to_string('email.txt', { 'appn':obj })
        msg_html = render_to_string('email.html', { 'appn':obj })

        #I used EmailMultiAlternatives because I wanted to send both text and html
       
        emailMessage = EmailMultiAlternatives(subject=subject, body=msg_plain, from_email=from_email, to=to_list)
        emailMessage.attach_alternative(msg_html, "text/html")
        emailMessage.content_subtype = 'html'
        emailMessage.mixed_subtype = 'related'

        image_file = open(image_path, 'rb')
        msg_image = MIMEImage(image_file.read())
        image_file.close()
        msg_image.add_header('Content-ID', '<image1>')
        emailMessage.attach(msg_image)
       
        image_file1 = open(image_path1, 'rb')
        msg_image1 = MIMEImage(image_file1.read())
        image_file1.close()
        msg_image1.add_header('Content-ID', '<image2>')
        emailMessage.attach(msg_image1)
       

        emailMessage.send(fail_silently=False)
        return redirect('myactivities')
        
    else:
        return redirect('placeorder')

def srchourcollection(request,cnt):
    prdtyp = Product_Type.objects.all()
    prd = Products.objects.all()

    

    if request.method == 'GET':
        return render(request,'Collections.html',{'products':prd , 'prodtyp':prdtyp})
    else:
        if cnt == '0':
            prd = Products.objects.all()
        else:
            prd = Products.objects.filter(description__icontains=request.POST['search'])

        return render(request,'Collections.html',{'products':prd , 'prodtyp':prdtyp})    
    

@login_required
def delcart(request, ord_pk):
    prd = Products.objects.filter(Product_Type=ord_pk)
    prdtyp = Product_Type.objects.all()
    if request.method == 'POST':
        try:
            try:
                prdtrn = Transact_hdr.objects.get(Status='Pending',user=request.user)
                cart_id = prdtrn.id
            except Transact_hdr.DoesNotExist:
                return render(request,'nocart.html',{'prodtyp': prdtyp})

            Tran_del = Transact_dtl.objects.get(pk=ord_pk)
            Tran_del.delete()
            
            cart = Transact_dtl.objects.filter(Transact_id=prdtrn)
            total_price = Transact_dtl.objects.filter(Transact_id=prdtrn).aggregate(Sum('Current_Rate'))

            return render(request,'mycart.html',{'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': total_price })
        except IntegrityError:
                return render(request,'Collections.html',{'products':ord_pk , 'prodtyp':prdtyp, 'error': 'Some error'})

@staff_member_required
def delcart1(request, ord_pk):
    prd = Products.objects.filter(Product_Type=ord_pk)
    prdtyp = Product_Type.objects.all()
    if request.method == 'POST':
        try:
            Tran_del = Transact_dtl.objects.get(pk=ord_pk)
            prdtrn = Tran_del.Transact_id 
            Tran_del.delete()

            total_price = Transact_dtl.objects.filter(Transact_id=prdtrn).aggregate(Sum('Current_Rate'))
            decimal_val = float(total_price['Current_Rate__sum'])    
            prdtrn.Amount = decimal_val
            prdtrn.save()
                        
            return redirect('OrderList')  
        except IntegrityError:
                return redirect('OrderList')  

@login_required
def confirmation(request):
    prdtyp = Product_Type.objects.all()
    if request.method == 'POST':
        try:
            prdtrn = Transact_hdr.objects.get(Status='Pending',user=request.user)
            cart_id = prdtrn.id
        except Transact_hdr.DoesNotExist:
            return render(request,'nocart.html',{'prodtyp': prdtyp})

        total_price = Transact_dtl.objects.filter(Transact_id=prdtrn).aggregate(Sum('Current_Rate'))
        decimal_val = float(total_price['Current_Rate__sum'])    
        prdtrn.Amount = decimal_val
        prdtrn.Mobile = request.POST['mobile']
        prdtrn.Status = 'InProgress'
        prdtrn.Datecompleted = date.today()
        prdtrn.save()

        cust= prdtrn.user.first_name
        cart = Transact_dtl.objects.filter(Transact_id=prdtrn)
        

        # mailing login
        subject = 'Order No. ' + str(cart_id) + ' placed successfully'
        
        usr= request.user
        ap_email = usr.email  

        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER, ap_email]

        #image_path = 'C:\Python\Artique\ArtiqueApp\static\images\Artique.jpg'
        image_path = settings.MEDIA_ROOT + '\ArtiqueApp\static\images\Artique.jpg'
        image_path1 = settings.MEDIA_ROOT + '\ArtiqueApp\static\images\Art_Attach.jpg'
        image_name = Path(image_path).name
        image_name1 = Path(image_path1).name
        
            
        msg_plain = render_to_string('email.txt', {'Mobileno':prdtrn.Mobile, 'Cust': cust,'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': decimal_val })
        msg_html = render_to_string('email1.html', {'pd':prdtrn,'Mobileno':prdtrn.Mobile, 'Cust': cust,'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': decimal_val })

        #I used EmailMultiAlternatives because I wanted to send both text and html
       
        emailMessage = EmailMultiAlternatives(subject=subject, body=msg_plain, from_email=from_email, to=to_list)
        emailMessage.attach_alternative(msg_html, "text/html")
        emailMessage.content_subtype = 'html'
        emailMessage.mixed_subtype = 'related'

        image_file = open(image_path, 'rb')
        msg_image = MIMEImage(image_file.read())
        image_file.close()
        msg_image.add_header('Content-ID', '<image1>')
        emailMessage.attach(msg_image)
       
        image_file1 = open(image_path1, 'rb')
        msg_image1 = MIMEImage(image_file1.read())
        image_file1.close()
        msg_image1.add_header('Content-ID', '<image2>')
        emailMessage.attach(msg_image1)
       

        emailMessage.send(fail_silently=False)

     
        #return render(request,'email.html',{'Mobileno':prdtrn.Mobile, 'Cust': cust,'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': total_price })

        return render(request,'Confirmation.html',{'Mobileno':prdtrn.Mobile, 'Cust': cust,'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': total_price })
    else:
         return render(request,'ContactUs.html',{'prodtyp':prdtyp})

@staff_member_required
def cancelled(request,ord_pk):
    prdtyp = Product_Type.objects.all()
    if request.method == 'POST':
        prdtrn = get_object_or_404(Transact_hdr,pk=ord_pk)
        prdtrn.Status = 'Cancelled'
        prdtrn.save()

    return redirect('OrderList') 


@staff_member_required
def delivered(request,ord_pk):
    prdtyp = Product_Type.objects.all()
    if request.method == 'POST':
        prdtrn = get_object_or_404(Transact_hdr,pk=ord_pk)
        cart_id = prdtrn.id
        
        prdtrn.Status = 'Completed'
        prdtrn.save()

        cust= prdtrn.user.first_name
        cart = Transact_dtl.objects.filter(Transact_id=prdtrn)
        
        total_price = Transact_dtl.objects.filter(Transact_id=prdtrn).aggregate(Sum('Current_Rate'))
        decimal_val = float(total_price['Current_Rate__sum'])    
       

        # mailing login
        subject = 'Order No. ' + str(cart_id) + ' is delivered'
        
        usr= request.user
        ap_email = usr.email  

        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER, ap_email]

        #image_path = 'C:\Python\Artique\ArtiqueApp\static\images\Artique.jpg'
        image_path = settings.MEDIA_ROOT + '\ArtiqueApp\static\images\Artique.jpg'
        image_path1 = settings.MEDIA_ROOT + '\ArtiqueApp\static\images\Art_Attach.jpg'
        image_name = Path(image_path).name
        image_name1 = Path(image_path1).name
        
            
        msg_plain = render_to_string('email.txt', {'Mobileno':prdtrn.Mobile, 'Cust': cust,'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': decimal_val })
        msg_html = render_to_string('email1.html', {'pd':prdtrn,'Mobileno':prdtrn.Mobile, 'Cust': cust,'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': decimal_val })

        #I used EmailMultiAlternatives because I wanted to send both text and html
       
        emailMessage = EmailMultiAlternatives(subject=subject, body=msg_plain, from_email=from_email, to=to_list)
        emailMessage.attach_alternative(msg_html, "text/html")
        emailMessage.content_subtype = 'html'
        emailMessage.mixed_subtype = 'related'

        image_file = open(image_path, 'rb')
        msg_image = MIMEImage(image_file.read())
        image_file.close()
        msg_image.add_header('Content-ID', '<image1>')
        emailMessage.attach(msg_image)
       
        image_file1 = open(image_path1, 'rb')
        msg_image1 = MIMEImage(image_file1.read())
        image_file1.close()
        msg_image1.add_header('Content-ID', '<image2>')
        emailMessage.attach(msg_image1)
       

        emailMessage.send(fail_silently=False)

     
        #return render(request,'email.html',{'Mobileno':prdtrn.Mobile, 'Cust': cust,'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': total_price })

        return redirect('OrderList')  
    else:
        return redirect('OrderList')  

@login_required
def mycart(request, prod_pk):
    prdtyp = Product_Type.objects.all()
    if request.method == 'POST':
        try:
            #cart_id=request.session.get('ART_Cart_id','0')
            try:
             prdtrn = Transact_hdr.objects.get(Status='Pending',user=request.user)
             cart_id = prdtrn.id
            except Transact_hdr.DoesNotExist:
                prdtrn = Transact_hdr(Status='Pending',user=request.user)
                prdtrn.save()
                cart_id = prdtrn.id
        
            prd_item = get_object_or_404(Products,pk=prod_pk)

            prdtrndtl = Transact_dtl(Transact_id=prdtrn, Product=prd_item, user=request.user, Current_Rate=prd_item.Current_Rate)
            prdtrndtl.save()

            
            cart = Transact_dtl.objects.filter(Transact_id=prdtrn)
            total_price = Transact_dtl.objects.filter(Transact_id=prdtrn).aggregate(Sum('Current_Rate'))

            return render(request,'mycart.html',{'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': total_price })
        except IntegrityError:
                return render(request,'Collections.html',{'products':prod_pk , 'prodtyp':prdtyp, 'error': 'Some error'})
    else:
        try:
            try:
             prdtrn = Transact_hdr.objects.get(Status='Pending',user=request.user)
             cart_id = prdtrn.id
            except Transact_hdr.DoesNotExist:
               return render(request,'nocart.html',{'prodtyp': prdtyp})
            
            cart = Transact_dtl.objects.filter(Transact_id=prdtrn)
            total_price = Transact_dtl.objects.filter(Transact_id=prdtrn).aggregate(Sum('Current_Rate'))
            return render(request,'mycart.html',{'Cart': cart , 'CartId': cart_id , 'prodtyp':prdtyp, 'Totalprice': total_price })
        except Http404:
                return render(request,'nocart.html',{'prodtyp': prdtyp})

def gallery(request):
    prdtyp = Product_Type.objects.all()
    return render(request,'Gallery.html',{'prodtyp':prdtyp})  

def loginuser(request):
    if request.method == 'GET':
        return render(request,'Loginuser.html', {'form': AuthenticationForm()})
    else:
        usr = authenticate(request, username=request.POST['username'] ,password=request.POST['password']  )
        if usr is None:
            return render(request,'Loginuser.html', {'form': AuthenticationForm(), 'error':'Please check entered username & password'})
        else:
            login(request,usr)
            return redirect('artiquehome')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('ahome')
    
        
    
              