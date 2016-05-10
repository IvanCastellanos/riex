from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify

# Catalog related app

#Upload location
def image_upload_location( instance, filename ):
    if(instance.__class__.__name__ is 'Product'):
        return "%s/%s/%s/%s" % ( (instance.category.__class__.__name__),
                                  instance.category.slug,
                                  instance.slug,
                                  filename )
    else:
        return "%s/%s/%s" % ( (instance.__class__.__name__), 
                               instance.slug, 
                               filename )


#Category is related to all of the other things
class Category( models.Model ):
    title       = models.CharField( max_length = 50, 
                                    unique     = True,
                                    null       = False, 
                                    blank      = False, )

    slug        = models.SlugField( unique     = True,
                                    null       = False, )

    image       = models.ImageField( upload_to = image_upload_location,
                                     default   = 'static/default_category.png',
                                     null      = False,
                                     blank     = True, )

    description = models.TextField( null       = True,
                                    blank      = True, )

    
    def __str__( self ):
        return self.title



#Default product
def get_default_product():
    return Category.objects.get_or_create( title       = 'Sin categoria',
                                           description = 'Productos sin categoria', )[0]

#Product
class Product( models.Model ):
    title       = models.CharField( max_length = 75,
                                    unique     = True,     #Products must have different title
                                    null       = False, 
                                    blank      = False, )

    slug        = models.SlugField( unique     = True,
                                    null       = False, )

    image       = models.ImageField( upload_to = image_upload_location,
                                     default   = 'static/default_product.png',
                                     null      = False,
                                     blank     = True, )

    #Description is optional
    description = models.TextField( null  = True,
                                    blank = True, )

    category    = models.ForeignKey( 'Category',
                                     default   = get_default_product,
                                     on_delete = models.SET_DEFAULT, 
                                     null      = False,
                                     blank     = False, )
    
    #Price of a product can't exceed $99,999.99
    price       = models.DecimalField( max_digits     = 7,
                                       decimal_places = 2,
                                       null           = False,
                                       blank          = False, )

    stock       = models.PositiveSmallIntegerField( null  = False,
                                                    blank = False, )

    #The admin is able to show/hide a product to the user
    show        = models.BooleanField( default = True,
                                       null    = False,
                                       blank   = False, )

    UNIT_OF_WEIGHT_MEASUREMENT = (
        ('Mass', (
                ('Kg', 'kg'),
                ('Gr', 'gr'),
                ('Oz', 'oz'),
                ('Lbs', 'lbs'),
            )
        ),
        ('Capacity', (
                ('Ls', 'ls'),
                ('Mls', 'mls'),
                ('Gl', 'gl'),
            )
        ),
    )

    weight_measurement = models.CharField( max_length = 4,
                                           choices    = UNIT_OF_WEIGHT_MEASUREMENT, 
                                           null       = True,
                                           blank      = True, )
    
    #Product can't be heavier than 9,999.99 kg/oz/lb/grams or litres, mililiters, gal
    weight      = models.DecimalField( max_digits     = 6,
                                       decimal_places = 2, 
                                       null           = True,
                                       blank          = True, )

    number_sales = models.PositiveIntegerField( blank = True,
                                                null  = True,
                                                default = 0,)

    def __str__( self ):
        return self.title


class Customer( models.Model ):
    company_name  = models.CharField( max_length = 50,
                                      unique     = True,
                                      null       = False,
                                      blank      = False, )

    rfc           = models.CharField( max_length = 13,
                                      unique     = True, 
                                      null       = False,
                                      blank      = False, )

    country       = models.CharField( max_length = 25,
                                      null       = False,
                                      blank      = False, )

    state         = models.CharField( max_length = 25,
                                      null       = False,
                                      blank      = False, )

    city          = models.CharField( max_length = 25,
                                      null       = False,
                                      blank      = False, )

    colony        = models.CharField( max_length = 100, 
                                      null       = False,
                                      blank      = False, )

    postal_code   = models.CharField( max_length = 5,
                                      null       = False,
                                      blank      = False, )
    
    street        = models.CharField( max_length = 100,
                                      null       = False, 
                                      blank      = False, )

    number        = models.CharField( max_length = 5,
                                      null       = False,
                                      blank      = False, )

    phone_number  = models.CharField( max_length = 17,
                                      null       = False,
                                      blank      = False, )

    email         = models.EmailField( null = False,
                                       blank = False, )

    creation_date = models.DateTimeField( auto_now     = False,
                                          auto_now_add = True, )


    def __str__(self):
        return self.company_name


class Product_unit( models.Model ):
    product = models.ForeignKey( 'Product', 
                                 on_delete = models.PROTECT,
                                 null     = False, 
                                 blank    = False, )

    quantity = models.PositiveSmallIntegerField( null  = False,
                                                 default = 1,
                                                 blank = False,)
    
    subtotal_cost = models.DecimalField( null = False,
                                         blank = False,
                                         max_digits = 9,
                                         decimal_places = 2,
                                         default = 0)


#Cotization
class Order( models.Model ):
    customer      = models.ForeignKey( 'Customer',
                                       on_delete = models.PROTECT,
                                       null      = False,
                                       blank     = False, )
    
    #FIX THIS
    products      = models.ManyToManyField( 'Product_unit' )

    creation_date = models.DateTimeField( auto_now     = False,
                                          auto_now_add = True, )

    approved_date = models.DateTimeField( auto_now     = True,
                                          auto_now_add = False,
                                          null         = True,)

    #Status types
    STATUS_TYPES = (
        ("en curso", "En curso"),
        ("no aprobado", "No aprobado"),
        ("entregado", "Entregado"),
        ("aprobado", "Aprobado"),
    )
    
    status        = models.CharField( max_length = 11,
                                      choices    = STATUS_TYPES,
                                      default    = STATUS_TYPES[0][0],
                                      null       = False,
                                      blank      = False, )
    
    #costs can't be larger than $ 9;999,999.99
    subtotal_cost = models.DecimalField( max_digits     = 9,
                                         decimal_places = 2, 
                                         null           = False, )
    
    total_cost    = models.DecimalField( max_digits     = 9,
                                         decimal_places = 2,
                                         null           = False, )

    details       = models.TextField( null  = True,
                                      blank = True, )

    
    def __str__(self):
        return self.customer.company_name





def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    if ((instance.__class__.__name__) == 'Product'):
        qs = Product.objects.filter(slug=slug).order_by("-id")
    elif ((instance.__class__.__name__) == 'Category'):
        qs = Category.objects.filter(slug=slug).order_by("-id")

    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug = new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Product)
pre_save.connect(pre_save_post_receiver, sender=Category)
