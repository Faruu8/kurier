from django.contrib import admin
from .models import Recipient, Customer, Courier, Package

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'postal_code', 'customer')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'address')

@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('customer', 'recipient', 'weight', 'description')

# Możesz dodać więcej modeli do zarządzania w panelu admina tutaj, używając dekoratora `@admin.register(Model)`
