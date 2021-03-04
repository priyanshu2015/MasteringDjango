from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

from .models import Cart, Product, ProductInCart, Order, ProductInOrder, Deal, Customer, Seller, Contact, SellerAdditional, OtpModel, PremiumProduct

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class SellerAdditionalInline(admin.TabularInline):
    model = SellerAdditional

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'name','type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),   #'is_customer' , 'is_seller'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'name', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class SellerAdmin(admin.ModelAdmin):
    inlines = (
        SellerAdditionalInline,
    )





#admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)


#admin.site.register(User, UserAdmin)


class ProductInCartInline(admin.TabularInline):
    model = ProductInCart

class CartInline(admin.TabularInline):
    model = Cart    #onetoonefield foreignkey

class DealInline(admin.TabularInline):
    model = Deal.user.through


# class UserAdmin(UserAdmin):
#     model = User
#     list_display = ('username', 'get_cart', 'is_staff', 'is_active',)
#     list_filter = ('username', 'is_staff', 'is_active', 'is_superuser')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Permissions', {'fields': ('is_staff', ('is_active' , 'is_superuser'), )}),
#         ('Important dates',{'fields': ('last_login', 'date_joined')}),
#         #('Cart', {'fields': ('get_cart',)})
#         ('Advanced options', {
#             'classes': ('collapse',),
#             'fields': ('groups', 'user_permissions'),
#         }),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),   # class for css 
#             'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups')}     # fields shown on create user page on admin panel
#         ),
#     )
#     inlines = [
#         CartInline, DealInline
#     ]
#     def get_cart(self,obj):       # this function only works in list_display
#         return obj.cart           # through reverse related relationship
#     search_fields = ('username',)     #search_filter for search bar
#     ordering = ('username',)

    







# from django.utils.html import format_html
# from django.urls import reverse
# def linkify(field_name):
#     """
#     Converts a foreign key value into clickable links.
    
#     If field_name is 'parent', link text will be str(obj.parent)
#     Link will be admin url for the admin url for obj.parent.id:change
#     """
#     def _linkify(obj):
#         linked_obj = getattr(obj, field_name)
#         if linked_obj is None:
#             return '-'
#         app_label = linked_obj._meta.app_label
#         model_name = linked_obj._meta.model_name
#         view_name = f'admin:{app_label}_{model_name}_change'
#         link_url = reverse(view_name, args=[linked_obj.pk])
#         return format_html('<a href="{}">{}</a>', link_url, linked_obj)

#     _linkify.short_description = field_name  # Sets column name
#     return _linkify



@admin.register(Cart) # through register decorator
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user','staff', 'created_on',)    # here user__is_staff will not work   
    list_filter = ('user', 'created_on',)
    #fields = ('staff',)           # either fields or fieldset
    fieldsets = (
        (None, {'fields': ('user', 'created_on',)}),   # only direct relationship no nested relationship('__') ex. user__is_staff
        #('User', {'fields': ('staff',)}),
    )
    inlines = (
        ProductInCartInline,
    )
    # To display only in list_display
    def staff(self,obj):
        return obj.user.is_staff
    # staff.empty_value_display = '???'
    staff.admin_order_field  = 'user__is_staff'  #Allows column order sorting
    staff.short_description = 'Staff User'  #Renames column head

    #Filtering on side - for some reason, this works
    list_filter = ['user__is_staff', 'created_on',]    # with direct foreign key(user) no error but not shown in filters, with function error
    # ordering = ['user',]
    search_fields = ['user__username']     # with direct foreign key no error but filtering not possible directly



# class DealAdmin(admin.ModelAdmin):
#     inlines = [
#         DealInline,
#     ]
#     exclude = ('user',)



class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder

@admin.register(Order) # through register decorator
class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = (
        ProductInOrderInline,
    )

#admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Deal)#, DealAdmin)
#admin.site.register(UserType)
admin.site.register(Customer)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Contact)
admin.site.register(SellerAdditional)


#1 using simple database for sessions 
from django.contrib.sessions.models import Session
import pprint

# If you remove this model admin below for sessions then you will see encrypted data only
# class SessionAdmin(admin.ModelAdmin):
#     def _session_data(self, obj):
#         return obj.get_decoded()
#     list_display = ['session_key', '_session_data', 'expire_date']
# admin.site.register(Session, SessionAdmin)

# class SessionAdmin(admin.ModelAdmin):
#     def _session_data(self, obj):
#         return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
#     _session_data.allow_tags=True
#     list_display = ['session_key', '_session_data', 'expire_date']
#     readonly_fields = ['_session_data']
#     exclude = ['session_data']
#     date_hierarchy='expire_date'

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']

admin.site.register(Session, SessionAdmin)

admin.site.register(ProductInOrder)

#admin.site.register(Session)


#from django.contrib.sites.models import Site
#admin.site.register(Site)


# from django_cache.models import my_cache_table
# admin.site.register(my_cache_table)


admin.site.register(OtpModel)
admin.site.register(PremiumProduct)