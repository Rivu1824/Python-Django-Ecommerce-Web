from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    ordering = ('-date_joined',)

admin.site.register(User, UserAdmin)

class CategorieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'description', 'slug']
    search_fields = ['title', 'description', 'slug']
admin.site.register(Categorie, CategorieAdmin)

class SubCategorieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'parent_categorie', 'description', 'slug']
    search_fields = ['title', 'parent_categorie__title', 'description', 'slug']
admin.site.register(SubCategorie, SubCategorieAdmin)

class ThirdCategorieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'parent_subcategorie', 'description', 'slug']
    search_fields = ['title', 'parent_subcategorie__title', 'description', 'slug']
admin.site.register(ThirdCategorie, ThirdCategorieAdmin)


class ProductPointInline(admin.StackedInline):
    model = Product_point
    list_display = ['point']
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_title', 'price', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'categories', 'level']
    search_fields = ['title', 'sub_title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductPointInline]




class Product_SpecificationAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Guarantee', 'Brand', 'Item_model_number')  
    list_filter = ('Product', 'Brand')                                     
    search_fields = ('Guarantee', 'Brand', 'Item_model_number')             

admin.site.register(Product_Specification, Product_SpecificationAdmin)




class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered', 'color','size','item', 'quantity', 'get_final_price')

admin.site.register(OrderItem, OrderItemAdmin)


class LogoAdmin(admin.ModelAdmin):
    list_display = ('id','Logo_file', 'nav_image','background_image','email', 'address', 'mobile_number', 'facebook_link', 'linkedin_link', 'instagram_link')

admin.site.register(Logo, LogoAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sub_title', 'description')

admin.site.register(Banner, BannerAdmin)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','created_at']
    search_fields = ['name', 'email', ]
    list_filter = ['created_at']



@admin.register(OrderItemSuccess)
class OrderItemSuccessAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'color', 'size', 'quantity', 'get_final_price']
    list_filter = ['color', 'size']
    search_fields = ['order__user__username', 'product__title']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_id', 'amount', 'payment_status', 'timestamp']
    list_filter = ['payment_status', 'timestamp']
    search_fields = ['user__username', 'user__email', 'transaction_id', 'mobile']

admin.site.register(Order, OrderAdmin)



class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount']
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)