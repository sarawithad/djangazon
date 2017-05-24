from django.test import client, TestCase
from website.models import *
from website.views import *
from django.urls import reverse


class ProductDetailViewTest(TestCase):

    def setUp(self):
        customer = Customer.objects.create(
            first_name = "Meg",
            last_name = "Ducharme",
            user_name = "mducharme",
            email_address = "meg@meg.com",
            password = "abcd1234"
        )

        product_type = ProductType.objects.create(category_name="Test")

        self.product = Product.objects.create(
            seller = self.customer,
            product_type = product_type,
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
        self.assertEqual(response.context['product'].name, 'emoji stickers')


    def test_product_detail_view_shows_product_details(self):
        response = self.client.get(reverse('website:single_product', args=([self.product.pk])))
        self.assertContains(response, "emoji stickers")
        self.assertContains(response, "yay!")
        self.assertContains(response, "1.99")
        self.assertContains(response, "500")




