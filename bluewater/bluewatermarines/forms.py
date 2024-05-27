from django import forms
from .models import *
from django.contrib.auth.forms import *
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


User = get_user_model()


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        
    username = forms.CharField(
        max_length=150
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )




class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model

        if model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with the Username already exists")

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model

        if model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with the Email already exists")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
    

class CartForm(forms.Form):
    color = forms.CharField(max_length=100)
    size = forms.CharField(max_length=100)
    quantity = forms.IntegerField(initial=1)



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'mobile', 'address', 'city','Country','Postcode_Zip','State','Street_Address']


class CouponForm(forms.Form):
    code = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coupon code'}))