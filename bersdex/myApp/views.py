from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext


from .models import Products, Category
from .forms import ProductForm


# List
def product_list(request):
    queryset_list = Products.objects.all() #.order_by("-created_at")

    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(body__icontains=query)|
            Q(features__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            ).distinct()
    
    # paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    # page = request.GET.get('page')
    # queryset = paginator.get_page(page)

    categories = Category.objects.all()

    paginator = Paginator(queryset_list, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)        
    
    context = {
        'title': 'List Of Products',
        'product_list': queryset,
        'categories': categories
    }

    return render(request, 'index.html', context)
  

# Details
def product_detail(request, slug=None):

    instance = get_object_or_404(Products, slug=slug)   

    context = {
        'instance': instance
    } 

    return render(request, 'detail.html', context)

# Create
def product_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
 
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        #Success Message
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'Not Successfully Created')    
        
    context = {
        'form': form
    }
    return render(request, 'create.html', context)

# Update
def product_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Products, slug=slug)   
    form = ProductForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Item Saved')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': instance.title,
        'instance': instance,
        'form': form
    }
    return render(request, 'create.html', context) 

def product_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instence = get_object_or_404(Products, slug=slug)
    instence.delete()
    messages.success(request, 'Deleted!')
    return redirect('list')

def category_details(request, slug):
    template = 'categories.html'
    category = get_object_or_404(Category, slug=slug)
    product = Products.objects.filter(category=category)
    category_list = Category.objects.all()

    context = {
        'category': category,
        'products': product,
        'category_list': category_list
    }

    return render(request, template, context)

