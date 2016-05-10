from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from django import forms
from django.utils import timezone
import datetime
import decimal
from django.forms.widgets import HiddenInput

#PDF generation related stuff wahaha
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

#Needed for email
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
from .forms import CustomerForm, OrderForm, ProductForm, Product_unitForm, CategoryForm

from .models import Product, Category, Product_unit, Customer, Order

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def order_pdf(request, id):
    #Retrieve data or whatever you need
    
    order = get_object_or_404(Order,id = id)
    products = order.products.all()

    return render_to_pdf(
            "shopping/order_pdf.html",
            {
                'pagesize':'A4',
                'order': order,
                'all_products': products,
            }
        )

@login_required
def index(request):
    
    #Customer
    #numero de ordenes
    #quien ha comprado mas####

    #Pedidos
    #con fecha y cantidad
    
    orders = Order.objects.filter(creation_date__year=2016)

    most_sell_products = Product.objects.order_by('-number_sales')[:8]
    
    customers = Customer.objects.all()[:8]

    total_sales = 0
    total_orders = 0

    for order in orders:
        total_sales += order.total_cost
        total_orders += 1

    average_sales = round(decimal.Decimal(total_sales / total_orders),2)
        
    context = {
        'total_orders':total_orders,
        'total_sales':total_sales,
        'average_sales':average_sales,
        'most_sell_products':most_sell_products,
        'customers':customers,
    }

    return render(request, "shopping/index.html", context)

@login_required
def product_detail(request, id_category=None, id_product=None):
    actual_product = Product.objects.get(id = id_product)
    last_order = Order.objects.last()
    #Has an actual customer
    #FORM
    form_product_unit = Product_unitForm(request.POST or None, initial={'product' : actual_product})


    if form_product_unit.is_valid():
        instance_product_unit = form_product_unit.save(commit=False)
        instance_product_unit.subtotal_cost = instance_product_unit.quantity * instance_product_unit.product.price
        instance_product_unit.save()

        last_order.products.add(instance_product_unit)
    
 
        last_order.subtotal_cost += instance_product_unit.subtotal_cost
        last_order.save()
        
        last_order.total_cost = round((last_order.subtotal_cost * decimal.Decimal(1.16)),2)
        last_order.save()

        return redirect('shopping:order_actual')

    is_buying = False
    if(last_order.status == "en curso"):
        is_buying = True
    
    context = {
        "Product" : actual_product,
        "Is_buying" : is_buying,
        "Last_order": last_order,
        #FORMS
        "form_product_unit" : form_product_unit,
    }
    return render(request, "shopping/product_detail.html", context)

@login_required
def products_list(request, id=None):
    query = Product.objects.filter(category = id)
    category = Category.objects.get(id = id)

    search = request.GET.get("q")
    if search:
        query = query.filter(title__icontains=search)
    
    context  = {
        "Products" : query,
        "Category": category,
    }
    return render(request, "shopping/products_list.html", context)

@login_required
def product_create_from_category(request, id):
    form = ProductForm(request.POST or None, request.FILES or None)
    
    category = Category.objects.get(id=id)
    
    if form.is_valid():
        instance = form.save(commit=False)
        #Terminar lo de la categoria actual
        instance.category = category
        instance.save()

        return redirect('shopping:products_list', category.id)
    
    context = {
        'form' : form,
        'Category': category,
    }

    return render(request, "shopping/product_create.html", context)
    
@login_required
def categories_list(request):
    query = Category.objects.all()
    
    search = request.GET.get("q")

    if search:
        query = query.filter(title__icontains=search)

    context = {
        "Categories": query,
    }

    return render(request, "shopping/categories_list.html", context)

@login_required
def category_create(request):
    form = CategoryForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        return redirect('shopping:categories_list')

    context = {
        'form':form,
    }

    return render(request, "shopping/category_create_form.html", context)

#def category_edit(request):
    

########Order part#####
@login_required
def customer_list(request):
    query = Customer.objects.all()

    context = {
        "Customers" : query,
    }

    return render(request, "shopping/customer_list.html", context)

@login_required
def customer_detail(request, id=None):
    customer = get_object_or_404(Customer, id=id)
    
    context = {
        "Customer": customer,
    }

    return render(request, "shopping/customer_detail.html", context)

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        return redirect('shopping:customer_list')

    context = {
        'form': form,
    }

    return render(request, "shopping/customer_create_form.html", context)

@login_required
def order_actual(request):
    
    last_order = Order.objects.last()

    iva = round(((last_order.total_cost) - (last_order.subtotal_cost)),2)

    if last_order.status != "en curso":
        raise Http404
    
    order_form = OrderForm(request.POST or None)

    if request.POST:
        if request.POST.get('success'):
            last_order.status = Order.STATUS_TYPES[-1][0]
            last_order.approved_date = timezone.localtime(timezone.now())
            last_order.save()
            
            for product in last_order.products.all():
                product.product.stock -= product.quantity
                product.product.number_sales += product.quantity
                product.product.save()
                
            new_last_order = Order.objects.last()

            #SENDS EMAIL TO THE CLIENT
            subject = '%s, su orden esta siendo procesada' % (new_last_order.customer.company_name) 
            contact_message = '''%s''' % ('Orden riex')
            from_email = settings.EMAIL_HOST_USER
            to_email = [new_last_order.customer.email]

            template_mail = """
            <h1>Su orden fue recibida</h1>
            """

            send_mail(subject, contact_message, from_email, to_email, html_message = template_mail, fail_silently=False)

            #Redirect to the last order
            return redirect('shopping:order_detail', new_last_order.id)
            
                            
    context = {
        'last_order': last_order,
        'order_form': order_form,
        'iva':iva,
    }
    
    return render(request, "shopping/order_actual_form.html", context)

@login_required
def order_create(request):
    last_order = Order.objects.last()

    order_form = OrderForm(request.POST or None, initial={'subtotal_cost': 0.0, 'total_cost': 0.0})
    
    #Hide unnecesary fields
    order_form.fields['status'].widget = forms.HiddenInput()
    order_form.fields['details'].widget = forms.HiddenInput()
    
    is_buying = False
    if (last_order.status == "en curso"):
        is_buying = True
    
    if request.POST:

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            #redirect to categories list
            return redirect('shopping:categories_list')
            
    
    context = {
        'order_form': order_form,
        'last_order': last_order,
        'Is_buying': is_buying,
    }

    return render(request, "shopping/order_create_form.html", context)

@login_required
def order_list(request):
    query = Order.objects.all()
    context = {
        "Orders": query,
    }
    
    return render(request, "shopping/order_list.html", context)

@login_required
def order_detail(request, id=None):
    order = get_object_or_404(Order,id = id)
    products = order.products.all()

    iva = round(((order.total_cost) - (order.subtotal_cost)),2)
   
    context = {
        "order":order,
        "all_products": products,
        "iva": iva,
    }

    return render(request, "shopping/order_detail.html", context)

@login_required
def help_view(request):
    return render(request, "shopping/help.html")
