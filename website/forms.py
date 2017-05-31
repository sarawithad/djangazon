from django.contrib.auth.models import User
from django import forms
from website.models import Product
from website.models import PaymentType
from website.models import Order


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

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