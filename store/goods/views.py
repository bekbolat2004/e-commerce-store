from django.shortcuts import render

# Create your views here.

from goods.models import Products



def catalog(request):

    goods = Products.objects.all()

    context = {
        'title': "Home - Category ",
        'goods': goods,

    }

    return render(request, 'catalog.html', context)

def product(request):
    return render(request, 'product.html')
