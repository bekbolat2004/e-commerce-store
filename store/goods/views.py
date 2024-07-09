from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

# Create your views here.

from goods.models import Products



def catalog(request, catalog_slug, page=1):

    if catalog_slug == 'all':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=catalog_slug))

    paginator = Paginator(goods, 3)

    cur_page = paginator.page(page)
    context = {
        'title': "Home - Category ",
        'goods': cur_page,
        'slug_url': catalog_slug,
    }

    return render(request, 'catalog.html', context)

def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    context = {
        'product': product
    }
    return render(request, 'product.html', context=context)
