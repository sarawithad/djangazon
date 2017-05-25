from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from website.forms import UserForm, ProductForm, PaymentTypeForm, OrderForm
from website.models import Product
from website.models import ProductType
from website.models import Profile
from website.models import PaymentType
from website.models import Order, ProductOrder
# standard Django view: query, template name, and a render method to render the data from the query into the s

def index(request):
    """
    Purpose: renders the index page with a list of 20 (mpax)  products
    Author: Harper Frankstone
    Args: request -- the full HTTP request object
    Returns: rendered view of the index page, with a list of products
    """
    all_products = Product.objects.all().order_by('-id')[:20]
    template_name = 'index.html'
    return render(request, template_name, {'products': all_products})


def register(request):
    """Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    """

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        template_name = 'register.html'
        return render(request, template_name, {'user_form': user_form})


def login_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return HttpResponseRedirect('/')

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    return render(request, 'login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def sell_product(request):
    """
    Purpose: to present the user with a form to upload information about a product to sell
    Author: Boilerplate code
    Args: request -- the full HTTP request object
    Returns: a form that lets a user upload a product to sell
    """
    if request.method == 'GET':
        product_form = ProductForm()
        template_name = 'create.html'
        return render(request, template_name, {'product_form': product_form})

    elif request.method == 'POST':
        form_data = request.POST
        pt = ProductType.objects.get(pk=form_data['product_type'])
        p = Product(
            seller = request.user,
            title = form_data['title'],
            description = form_data['description'],
            price = form_data['price'],
            quantity = form_data['quantity'],
            product_type = pt,
        )
        p.save()
        template_name = 'success.html'
        return render(request, template_name, {})


def list_products(request):
    """
    Purpose: to render a view with a list of all products
    Author: Boilerplate code
    Args: request -- the full HTTP request object
    Returns: a rendered view of a list of products
    """
    all_products = Product.objects.all()
    template_name = 'list.html'
    return render(request, template_name, {'products': all_products})

def single_product(request, product_id):
    """
    purpose: Allows user to view product_detail view, which contains a very specific view
        for a singular product
        For an example, visit /product_details/1/ to see a view on the first product created
        displaying title, description, quantity, price/unit, and "Add to order" button

    author: Max Baldridge

    args: product_id: (integer): id of product we are viewing 

    returns: (render): a view of the request, template to use, and product obj
    """        
    template_name = 'single.html'
    product = get_object_or_404(Product, pk=product_id)            
    return render(request, template_name, {
        "product": product})

def list_product_types(request):
    """
    Purpose: To retrieve a list of all products & product_types from
    their respective tables so that a template may sort through and filter
    the results.
    Author: Jordan Nelson
    Args: None
    Returns: Combines a given template with a given context dictionary and 
    returns an HttpResponse object with that rendered text.
    """
    product_types = ProductType.objects.all().order_by('-pk')

    for pt in product_types:
        pt.num_products = pt.product_set.filter(product_type=pt.id).count()
        pt.products = pt.product_set.filter(product_type=pt.id).order_by('-pk')[:3]

    return render(request, 'product_types.html', {'product_types': product_types})

def get_product_types(request, type_id):
    """
    Purpose: To allow a hyperlink to a specific URL (with the parameter type_id)
    to display a product category, and a list of products assigned to that category
    and their products.
    Author: Jordan Nelson
    Args: type_id
    Returns: Combines a given template with a given context dictionary and 
    returns an HttpResponse object with that rendered text.
    """
    product_types = ProductType.objects.all().filter(pk=type_id)
    products_of_type = Product.objects.all().filter(product_type=type_id)

    context = { 'product_types' : product_types, 'products_of_type' : products_of_type }
    
    return render(request, 'product_type_products.html', context )

@login_required(login_url='/login')
def profile(request): 
    """
    Purpose: to render the profile page in the browser
    Author: Harper Frankstone
    Args: request -- the full HTTP request object
    Returns: 
    """
    template_name = 'profile.html'
    return render(request, template_name, {})


@login_required(login_url='/login')
def add_payment_type(request):
    """
    Purpose: to present the user with a form to add a payment type to their account
    Author: Aaron Barfoot
    Args: request -- the full HTTP request object
    Returns: a form that lets a user add a payment type to their account
    """
    if request.method == 'GET':
        payment_type_form = PaymentTypeForm()
        template_name = 'add_payment_type.html'
        return render(request, template_name, {'payment_type_form': payment_type_form})

    elif request.method == 'POST':
        form_data = request.POST
        pmt = PaymentType(
            customer = request.user,
            payment_type_name = form_data['payment_type_name'],
            account_number = form_data['account_number'],
        )
        pmt.save()
        template_name = 'payment_type_success.html'
        return render(request, template_name, {})

@login_required(login_url='/login')
def user_payment_types(request):
    """
    Purpose: To retrieve a list of all payment types associated with user
    Author: Aaron Barfoot
    Args: request -- the full HTTP request object
    Returns: list of payment types associated with current user.
    """
    user_payment_types = PaymentType.objects.filter(customer = request.user)
    template_name = 'user_payment_types.html'
    return render(request, 'user_payment_types.html', {'user_payment_types': user_payment_types})

@login_required(login_url='/login')
def add_product_to_order(request, product_id):
    """
    Purpose: To add a product (by the product id) to the ProductOrder table.
    Author: Jordan Nelson & Harper Frankstone
    Args: product_id - the id of the product to be added to the cart
    Returns: Redirects user to their shopping cart after a successful add
    """
    product_to_add = Product.objects.get(pk=product_id)

    try:
        customer = request.user
        new_order = Order.objects.get(customer=customer, active=1)
    except ObjectDoesNotExist:
        customer = request.user
        new_order = Order.objects.create(customer=customer, order_date=None, payment_type=None, active=1)

    add_to_ProductOrder = ProductOrder.objects.create(product=product_to_add, order=new_order)

    return HttpResponseRedirect('/cart')

@login_required(login_url='/login')
def view_cart(request):
    """
    Purpose: To view the cart of a customer's products
    Author: Jordan Nelson & Harper Frankstone
    Args: request --the full HTTP request object
    Returns: A list of the products added to a shopping cart and their total
    """
    total = 0

    try:
        customer = request.user
        order_id = Order.objects.get(customer=customer, active=1).id
    except ObjectDoesNotExist:
        customer = request.user
        order_id = Order.objects.create(customer=customer, order_date=None, payment_type=None, active=1)

    try:
        products_in_cart = ProductOrder.objects.all().filter(order=order_id)
    except:
        return render(request, 'cart.html', { 'total' : total, 'orderid' : order_id } )

    for product in products_in_cart:
        total += product.product.price

    return render(request, 'cart.html', { 'products_in_cart' : products_in_cart, 'total' : total, 'orderid' : order_id } )

@login_required(login_url='/login')
def complete_order_add_payment(request, order_id):
    """
    purpose: Allows user to add a payment type to their order and therefore complete and place the order
    author: Harper Frankstone/Jordan Nelson
    args: request --the full HTTP request object, order_id - passed to this method from the view_cart method 
    returns: a checkout page where the user sees their order total and can select a payment type for their order
    """
    if request.method == 'POST':
        total = request.POST['total']
        adding_payment_types = PaymentType.objects.filter(customer = request.user)

        template_name = 'checkout.html'
        return render(request, template_name, { 'adding_payment_types': adding_payment_types, 'order_id' : order_id, 'total': total })

@login_required(login_url='/login')
def order_confirmation(request):
    """
    purpose: To mark an order as finished by setting the active field as 0 and writing the 
    payment type used for the order to the database.
    author: Jordan Nelson
    args: request --the full HTTP request object
    returns: renders the order confirmation table after a successful order completion
    """
    if request.method == 'POST':

        payment_type_id = request.POST['payment_type_id']
        order_id = request.POST['order_id']

        completed_order = Order.objects.get(pk=order_id)
        completed_order.payment_type = PaymentType.objects.get(pk=payment_type_id)
        completed_order.active = False
        completed_order.order_date = datetime.now()
        completed_order.save()        

        return render(request, 'order_confirmation.html' , {})

