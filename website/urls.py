from django.conf.urls import url

from . import views

app_name = "website"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^sell$', views.sell_product, name='sell'),
    url(r'^products$', views.list_products, name='list_products'),
    url(r'^single_product/(?P<product_id>[0-9]+)/$', views.single_product, name='single_product'),
    url(r'^product_types$', views.list_product_types, name='product_types'),
    url(r'^product_type_products/(?P<type_id>[0-9]+)/$', views.get_product_types, name='get_product_types'),
    url(r'^add_payment_type$', views.add_payment_type, name='add_payment_type'),
    url(r'^user_payment_types$', views.user_payment_types, name='user_payment_types'),
    url(r'^add_to_cart/(?P<product_id>[0-9]+)/$', views.add_product_to_order, name='add_product_to_order'),
    url(r'^cart$', views.view_cart, name='cart'),
    url(r'^checkout/(?P<order_id>[0-9]+)/$', views.complete_order_add_payment, name='checkout'),
    url(r'^order_confirmation$', views.order_confirmation, name='order_confirmation'),
    url(r'^delete_product_from_cart$', views.delete_product_from_cart, name='delete_product_from_cart'),
]