from django.test import client, TestCase
from website.models import *
from website.views import *
from django.urls import reverse

class ProductDetailViewTest(TestCase):
    """
    Purpose: Verify that when a product is created that the Product Detail view has the correct product with the product's title, description, price and quantity in the response context 
    Author: Dara Thomas
    Args: (integer) product pk
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username = "mducharme",
            email = "meg@meg.com",
            password = "abcd1234",
            first_name = "Meg",
            last_name = "Ducharme"
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
        self.assertQuerysetEqual(response.context['products_of_type'], ["<Product: Magic Hat>", "<Product: Magic Wand>"],ordered=False)

class PaymentTypesViewTest(TestCase):
    """
    Purpose: Verifies that the Payment Types view for a customer has all of the payment types in the request context
    Author: Dara Thomas
    Args: HTTP request
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """

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


    def test_payment_type_view_shows_payment_types(self):
        response = self.client.get(reverse('website:user_payment_types'))
        self.assertQuerysetEqual   (response.context["user_payment_types"], ["<PaymentType: AMEX>", "<PaymentType: MasterCard>", "<PaymentType: Visa>"])



class ProductsInCartViewTest(TestCase):
    """
    Purpose: Verify that when products are added to an order that the Order Summary view has those products in the response context
    Author: Dara Thomas
    Args: (integer) product pk
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """
        
    def test_products_show_in_cart(self):
        
        self.user = User.objects.create_user(
            username = "mducharme",
            email = "meg@meg.com",
            password = "abcd1234",
            first_name = "Meg",
            last_name = "Ducharme"
        )

        self.customer = Customer.objects.create(
            phone = 1234567890,
            user = self.user
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

        self.payment_type = PaymentType.objects.create(
            payment_type_name = "MasterCard",
            account_number = 5678567856785678,
            customer = self.user
        )

        self.order = Order.objects.create(
            customer = self.user,
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


        response = self.client.get(reverse('website:cart'))

        self.assertQuerysetEqual   (response.context["products_in_cart"], ["<ProductOrder: emoji stickers>", "<ProductOrder: Keys>", "<ProductOrder: Magic Wand>"])



class OrderHistoryViewTest(TestCase):
    """
    Purpose: to test that the order history is showing orders that correspond with the authenticated user
    Author: Harper Frankstone   
    Args: extends the TestCase 
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username = "jnelson",
            email = "jordo@jordo.com",
            password = "abcd1234",
            first_name = "Jordan",
            last_name = "Nelson"
        )

        self.customer = Customer.objects.create(
            phone = 1234567890,
            user = self.user
        )

        self.product_type = ProductType.objects.create(product_type_name="TestProdType")

        self.product = Product.objects.create(
            seller = self.user,
            product_type = self.product_type,
            title = "Beard Comb",
            description = "Finest Facial Comb in the Land",
            price = "5.25",
            quantity = "500"
        )

        self.order = Order.objects.create(
            customer = self.user,
        )

        self.product_order_1 = ProductOrder.objects.create(
            product = self.product,
            order = self.order
        )

    def test_order_history_view(self):
        response = self.client.get(reverse('website:order_detail', args=([self.product.pk])))
        print('The response: ', response)
        self.assertContains(response, "Beard Comb")
        self.assertContains(response, "5.25")
