from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from baskets.models import Basket
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

def _safe_return_url(request):
    candidate = request.POST.get("next") or request.META.get("HTTP_REFERER")
    if candidate and url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return reverse("user:users_basket")


@login_required
@require_POST
@transaction.atomic
def basket_add(request, product_slug):
    product = get_object_or_404(Products.objects.select_for_update(), slug=product_slug)
    if product.quantity < 1:
        messages.warning(request, "Товара сейчас нет в наличии.")
        return redirect(_safe_return_url(request))
    basket, created = Basket.objects.select_for_update().get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1},
    )
    if not created:
        if basket.quantity >= product.quantity:
            messages.warning(request, "В корзине уже доступное количество товара.")
            return redirect(_safe_return_url(request))
        basket.quantity += 1
        basket.save(update_fields=["quantity"])
    messages.success(request, "Товар добавлен в корзину.")
    return redirect(_safe_return_url(request))


@login_required
@require_POST
def basket_change(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id, user=request.user)
    try:
        quantity = int(request.POST.get("quantity", ""))
    except (TypeError, ValueError):
        messages.error(request, "Некорректное количество товара.")
        return redirect(_safe_return_url(request))

    if quantity < 1 or quantity > basket.product.quantity:
        messages.error(request, "Количество должно соответствовать доступному остатку.")
        return redirect(_safe_return_url(request))

    basket.quantity = quantity
    basket.save(update_fields=["quantity"])
    messages.success(request, "Количество товара обновлено.")
    return redirect(_safe_return_url(request))


@login_required
@require_POST
def basket_remove(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id, user=request.user)
    basket.delete()
    messages.success(request, "Товар удалён из корзины.")
    return redirect(_safe_return_url(request))
