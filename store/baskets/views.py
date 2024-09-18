# Create your views here.
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from baskets.models import Basket
# from baskets.utils import get_user_baskets
from goods.models import Products


# def basket_add(request):
#     product_id = request.POST.get("product_id")
#
#     product = Products.objects.get(id=product_id)
#
#     if request.user.is_authenticated:
#         baskets = Basket.objects.filter(user=request.user, product=product)
#
#         if baskets.exists():
#             basket = baskets.first()
#             if basket:
#                 basket.quantity += 1
#                 basket.save()
#         else:
#             Basket.objects.create(user=request.user, product=product, quantity=1)
#
#     else:
#         baskets = Basket.objects.filter(
#             session_key=request.session.session_key, product=product)
#
#         if baskets.exists():
#             basket = baskets.first()
#             if basket:
#                 basket.quantity += 1
#                 basket.save()
#         else:
#             Basket.objects.create(
#                 session_key=request.session.session_key, product=product, quantity=1)
#
#     user_basket = get_user_baskets(request)
#     basket_items_html = render_to_string(
#         "baskets/includes/included_basket.html", {"baskets": user_basket}, request=request)
#
#     response_data = {
#         "message": "Товар добавлен в корзину",
#         "basket_items_html": basket_items_html,
#     }
#
#     return JsonResponse(response_data)
#
#
# def basket_change(request):
#     basket_id = request.POST.get("basket_id")
#     quantity = request.POST.get("quantity")
#
#     basket = Basket.objects.get(id=basket_id)
#
#     basket.quantity = quantity
#     basket.save()
#     updated_quantity = basket.quantity
#
#     basket = get_user_baskets(request)
#     basket_items_html = render_to_string(
#         "baskets/includes/included_basket.html", {"baskets": basket}, request=request)
#
#     response_data = {
#         "message": "Количество изменено",
#         "basket_items_html": basket_items_html,
#         "quaantity": updated_quantity,
#     }
#
#     return JsonResponse(response_data)
#
#
# def basket_remove(request):
#     basket_id = request.POST.get("basket_id")
#
#     basket = Basket.objects.get(id=basket_id)
#     quantity = basket.quantity
#     basket.delete()
#
#     user_basket = get_user_baskets(request)
#     basket_items_html = render_to_string(
#         "baskets/includes/included_basket.html", {"baskets": user_basket}, request=request)
#
#     response_data = {
#         "message": "Товар удален",
#         "basket_items_html": basket_items_html,
#         "quantity_deleted": quantity,
#     }
#     return JsonResponse(response_data)

def basket_add(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user, product=product)

        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(user=request.user, product=product, quantity=1)

    return redirect(request.META['HTTP_REFERER'])



def basket_change(request, product_slug):
    pass


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return redirect(request.META['HTTP_REFERER'])
