from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Contact, Customer, Seller, SellerAdditional
from django import forms
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class ContactUsForm(forms.ModelForm):
    # email = forms.EmailField(required=True)
    # name = forms.CharField(max_length=5, required=True)
    
    # phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    # phone = forms.CharField(max_length=255, required=True, validators=[phone_regex])
    # query = forms.CharField(widget = forms.Textarea)
    class Meta:
        model = Contact
        fields = [
            'email',
            'phone',
            'query',
            'name'
        ]

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Seller
        fields = [
            'email',
            'name',
            'password1',
            'password2',
        ]

class RegistrationFormSeller(UserCreationForm):
    gst = forms.CharField(max_length=10)
    warehouse_location = forms.CharField(max_length=1000)
    class Meta:
        model = Seller
        fields = [
            'email',
            'name',
            'password1',
            'password2',
            'gst',
            'warehouse_location'
        ]

class RegistrationFormSeller2(forms.ModelForm):
    class Meta:
        model = SellerAdditional
        fields = [
            'gst',
            'warehouse_location'
        ]

























class RegistrationFormCustomer(UserCreationForm):
    class Meta:
        model = Customer
        fields = [
            'email',
            'name',
            'password1',
            'password2',
        ]