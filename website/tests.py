from django.test import client, TestCase
from website.models import *
from website.views import *
from django.urls import reverse


class ProductDetailViewTest(TestCase):
    """
    Purpose: Verify that when a product is created that the Product Detail view has the correct product with the product's title, description, price and quantity in the response context 
    Author: Dara Thomas
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


    def test_product_detail_view_shows_correct_product(self):
        response = self.client.get(reverse('website:single_product', args=([self.product.pk])))
        self.assertEqual(response.context['product'].title, 'emoji stickers')


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
    """
    Purpose: Verifies that the Payment Types view for a customer has all of the payment types in the request context
    Author: Dara Thomas
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


    def test_payment_type_view_shows_payment_types(self):
        response = self.client.get(reverse('website:user_payment_types'))
        self.assertQuerysetEqual   (response.context["user_payment_types"], ["<PaymentType: AMEX>", "<PaymentType: MasterCard>", "<PaymentType: Visa>"])



class ProductsInCartViewTest(TestCase):

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
            product_type = self.product_type,
            title = "emoji stickers",
            description = "yay!",
            price = 1.99,
            quantity = 500
        )

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


    def test_products_show_in_cart(self):
        response = self.client.get(reverse('website:view_cart'))
        self.assertQuerysetEqual   (response.context["products_in_cart"], ["<ProductOrder: emoji stickers>", "<ProductOrder: Magic Hat>", "<ProductOrder: Magic Wand>"])