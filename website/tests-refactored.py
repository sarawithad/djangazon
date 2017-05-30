from django.test import client, TestCase
from website.models import *
from website.views import *
from django.urls import reverse


class ProductRelatedTests(TestCase):
    """
    Purpose: Verifies that when a specific product category view is requested, that there are products in the response context. Also verifies that when a product is created that the Product Detail view has the correct product with the product's title, description, price and quantity in the response context.
    Author: Dara Thomas, Aaron Barfoot
    Args: (integer) product pk
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
            description = "oh oooh it's magic",
            price = 5.99,
            quantity = 12
        )

        self.product_3 = Product.objects.create(
            seller = self.user,
            product_type = self.product_type2,
            title = "emoji stickers",
            description = "yay!",
            price = 1.99,
            quantity = 50
        )

        self.client.login(
            username = "mscott",
            password = "1111"
        )

    def test_product_type_products_view(self):
        response = self.client.get(reverse('website:get_product_types', args=([self.product_type1.pk])))  
        self.assertQuerysetEqual(response.context['products_of_type'], ["<Product: Magic Wand>", "<Product: emoji stickers>"],ordered=False)


    def test_product_detail_view_shows_correct_product(self):
        response = self.client.get(reverse('website:single_product', args=([self.product.pk])))
        self.assertEqual(response.context['product'].title, 'emoji stickers')


    def test_product_detail_view_shows_product_details(self):
        response = self.client.get(reverse('website:single_product', args=([self.product_3.pk])))
        self.assertContains(response, "Magic Wand")
        self.assertContains(response, "oh oooh it's magic")
        self.assertContains(response, "10.99")
        self.assertContains(response, "3")
        self.assertContains(response, "emoji stickers")
        self.assertContains(response, "yay!")
        self.assertContains(response, "5.99")
        self.assertContains(response, "12")



class CustomerRelatedTests(TestCase):

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

        self.product_type = ProductType.objects.create(product_type_name="TestProdType")

        
        self.product_1 = Product.objects.create(
            seller = self.user,
            product_type = self.product_type,
            title = "emoji stickers",
            description = "yay!",
            price = 1.99,
            quantity = 500
        )


        self.product_2 = Product.objects.create(
            seller = self.user,
            product_type = self.product_type,
            title = "Keys",
            description = "They're keys",
            price = 3.00,
            quantity = 100
        )


        self.product_3 = Product.objects.create(
            seller = self.user,
            product_type = self.product_type,
            title = "Magic Wand",
            description = "oh oh it's magic",
            price = 5.99,
            quantity = 12
        )


        self.order = Order.objects.create(
            customer = self.user
        )

        self.product_order_1 = ProductOrder.objects.create(
            product = self.product_1,
            order = self.order
        )

        self.product_order_2 = ProductOrder.objects.create(
            product = self.product_2,
            order = self.order
        )


        self.product_order_3 = ProductOrder.objects.create(
            product = self.product_3,
            order = self.order
        )

        self.client.login(
            username = "mducharme",
            password = "abcd1234"
        )


    def test_payment_type_view_shows_payment_types(self):
        response = self.client.get(reverse('website:user_payment_types'))
        self.assertQuerysetEqual   (response.context["user_payment_types"], ["<PaymentType: AMEX>", "<PaymentType: MasterCard>", "<PaymentType: Visa>"])

    def test_products_show_in_cart(self):
        response = self.client.get(reverse('website:cart'))

        print(response.context["products_in_cart"])
        self.assertQuerysetEqual   (response.context["products_in_cart"], ["<ProductOrder: emoji stickers>", "<ProductOrder: Keys>", "<ProductOrder: Magic Wand>"])
