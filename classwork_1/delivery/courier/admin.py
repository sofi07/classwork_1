from django.contrib import admin

# Register your models here.
from .models import Client, Courier, Delivery


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('address', 'time', 'client', 'courier')