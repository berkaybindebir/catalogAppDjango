from django.conf import settings
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name


class Products(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    created_at = models.DateField(default=datetime.now, blank=True)
    image = models.FileField(upload_to=upload_location,
            null=True, 
            blank=True,)
    is_original = models.BooleanField(null=False)
    prod_date = models.DateField(null=True)
    features = models.CharField(max_length=200)
    sizes = models.CharField(max_length=10)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)  

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Product" 
        ordering = ["-id", "-created_at"]  

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})   

 

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Products.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug      

def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_product_receiver, sender=Products)      