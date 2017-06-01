from django.contrib.auth.models import User
from django import forms
from website.models import Product
from website.models import PaymentType
from website.models import Order
from website.models import Customer


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


# class CustomerProfile(forms.ModelForm):
#     username = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     phone = forms.IntegerField(required=True)
#     street_address = forms.CharField(required=True)

#     class Meta:
#         model = Customer
#         fields = ('phone', 'street_address')

#     def __init__(self, *args, **kwargs):
#         print(kwargs)
#         super(CustomerProfile, self).__init__(*args, **kwargs)
#         self.fields['user']=forms.ModelChoiceField(queryset=User.objects.all())


# class NewCustomerForm(forms.ModelForm):

#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = Customer
#         fields = ('username', 'first_name', 'last_name', 'email', 'password', 'phone', 'street_address')


class ProductForm(forms.ModelForm): 

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'quantity', 'product_type', 'product_photo', 'city',)

class PaymentTypeForm(forms.ModelForm):

	class Meta:
		model = PaymentType
		fields = ('payment_type_name', 'account_number')

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('payment_type',)