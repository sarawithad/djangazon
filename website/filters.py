from website.models import Product
import django_filters

class ProductFilter(django_filters.FilterSet):
    class Meta:
    	model = Product
    	fields = ['title']