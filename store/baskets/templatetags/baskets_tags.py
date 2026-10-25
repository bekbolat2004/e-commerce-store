from django import template
from baskets.models import Basket
from baskets.utils import get_user_baskets

register = template.Library()
@register.simple_tag()
def user_baskets(request):
    if request.user.is_authenticated:
        return get_user_baskets(request)
