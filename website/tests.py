from django.test import client, TestCase
from website.models import *
from website.views import *
from django.urls import reverse


class ProductDetailViewTest(TestCase):
    """
    Purpose:
    Author:
    Args:
    Returns: 
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username = "mducharme",
            email = "meg@meg.com",
            password = "abcd1234",
            first_name = "Meg",
            last_name = "Ducharme"
        )

        self.customer = Customer.objects.create(
            first_name = "Meg",
            last_name = "Ducharme",
            user_name = "mducharme",
            email_address = "meg@meg.com",
            password = "abcd1234"
        )

        self.product_type = ProductType.objects.create(product_type_name="Test")

        self.product = Product.objects.create(
            seller = self.user,
            product_type = self.product_type,
            title = "emoji stickers",
            description = "yay!",
            price = 1.99,
            quantity = 500
        )

        self.client.login(
            username = "mducharme",
            password = "abcd1234"
        )

    #Verify that when a product is created that the Product Detail view has the correct product in the response context
    def test_product_detail_view_shows_correct_product(self):
        response = self.client.get(reverse('website:single_product', args=([self.product.pk])))
        self.assertEqual(response.context['product'].title, 'emoji stickers')


    #Verify that when a product is created that the Product Detail view has the title, description, price and quantity are in the response body
    def test_product_detail_view_shows_product_details(self):
        response = self.client.get(reverse('website:single_product', args=([self.product.pk])))
        self.assertContains(response, "emoji stickers")
        self.assertContains(response, "yay!")
        self.assertContains(response, "1.99")
        self.assertContains(response, "500")

class ProductTypeViewTest(TestCase):
    """
    Purpose: Verify that when a specific product type is chosen, only products in that type are displayed.
    Author: Aaron Barfoot
    Args: (integer) product_type pk
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username = "mscott",
            email = "mike@dm.com",
            password = "1111",
            first_name = "Michael",
            last_name = "Scott"
        )

        self.product_type1 = ProductType.objects.create(product_type_name="TestType1")
        self.product_type2 = ProductType.objects.create(product_type_name="TestType2")

        self.product = Product.objects.create(
            seller = self.user,
            product_type = self.product_type1,
            title = "Magic Wand",
            description = "Getting Testy",
            price = 5.99,
            quantity = 12
        )

        self.product = Product.objects.create(
            seller = self.user,
            product_type = self.product_type1,
            title = "Magic Hat",
            description = "Getting Really Testy",
            price = 10.99,
            quantity = 3
        )

        self.product = Product.objects.create(
            seller = self.user,
            product_type = self.product_type2,
            title = "Non-Magic Hat",
            description = "Shouldn't show",
            price = 1.99,
            quantity = 1
        )


        self.client.login(
            username = "mscott",
            password = "1111"
        )

    def test_product_type_products_view(self):
        response = self.client.get(reverse('website:get_product_types', args=([self.product_type1.pk])))
        self.assertContains(response, 'TestType1')    
        self.assertContains(response, 'Magic Wand')    
        self.assertContains(response, 'Magic Hat')    





class PaymentTypesViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username = "mducharme",
            email = "meg@meg.com",
            password = "abcd1234",
            first_name = "Meg",
            last_name = "Ducharme"
        )

        self.payment_type = PaymentType.objects.create(
            payment_type_name = "Visa",
            account_number = 1234123412341234,
            customer = self.user
        )

        self.payment_type = PaymentType.objects.create(
            payment_type_name = "MasterCard",
            account_number = 5678567856785678,
            customer = self.user
        )

        self.payment_type = PaymentType.objects.create(
            payment_type_name = "AMEX",
            account_number = 1010101010101010,
            customer = self.user
        )

        self.client.login(
            username = "mducharme",
            password = "abcd1234"
        )


    #Verify that the Payment Types view for a customer has all of the payment types in the request context
    def test_payment_type_view_shows_payment_types(self):
        response = self.client.get(reverse('website:user_payment_types', args=([self.payment_type.pk])))
        self.assertContains(response, "Visa")
        self.assertContains(response, "MasterCard")
        self.assertContains(response, "AMEX")










