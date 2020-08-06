from django.contrib import admin
from .models import Products, Product_Type,Transact_hdr,Transact_dtl,Appointment,subscriber

admin.site.register(Products)
admin.site.register(Product_Type)
admin.site.register(Transact_hdr)
admin.site.register(Transact_dtl)
admin.site.register(Appointment)
admin.site.register(subscriber)

