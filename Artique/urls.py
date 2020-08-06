"""Artique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ArtiqueApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('^accounts/login/', admin.site.urls),

    path('ahome/', views.ahome,name='ahome'),
    path('artiquehome/', views.artiquehome,name='artiquehome'),
    path('appointment/', views.appointment,name='appointment'),
    path('contactus/', views.contactus,name='contactus'),
    path('confirmation/', views.confirmation,name='confirmation'),
    path('confirmappoint/', views.confirmappoint,name='confirmappoint'),    
    path('myactivities/', views.myactivities,name='myactivities'),    
    path('ourcollection/<int:prd_pk>', views.ourcollection,name='ourcollection'),
    path('srchourcollection/<str:cnt>', views.srchourcollection,name='srchourcollection'),
    path('delcart/<int:ord_pk>', views.delcart,name='delcart'),
    path('delcart1/<int:ord_pk>', views.delcart1,name='delcart1'),
    path('delivered/<int:ord_pk>', views.delivered,name='delivered'),
    path('cancelled/<int:ord_pk>', views.cancelled,name='cancelled'),
    path('mycart/<int:prod_pk>', views.mycart,name='mycart'),
    path('gallery/', views.gallery,name='gallery'),
    path('signupuser/', views.signupuser,name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('loginuser/', views.loginuser,name='loginuser'),
    path('logoutuser/', views.logoutuser,name='logoutuser'),
    path('confirmsubscribe/', views.confirmsubscribe,name='confirmsubscribe'),
    path('OrderList/', views.OrderList,name='OrderList'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
