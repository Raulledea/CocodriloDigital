from django.contrib import admin
from .models import Product, Promotion

class PromotionInline(admin.TabularInline):
    model = Promotion
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PromotionInline]

