from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

# Create your views here.

from goods.models import Products
from goods.utils import q_search

def catalog(request, catalog_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if catalog_slug == 'all':
        goods = Products.objects.all()
    elif query:
       goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=catalog_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by in {'price', '-price'}:
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    cur_page = paginator.get_page(page)
    context = {
        'title': "Home - Category ",
        'goods': cur_page,
        'slug_url': catalog_slug,
    }

    return render(request, 'catalog.html', context)

def product(request, product_slug):

    product = get_object_or_404(Products, slug=product_slug)

    context = {
        'product': product
    }
    return render(request, 'product.html', context=context)
