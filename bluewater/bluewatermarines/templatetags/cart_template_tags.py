from django import template
from bluewatermarines.models import OrderItem

register = template.Library()

@register.simple_tag
def cart_item_count(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user=user,ordered=False)
        if qs.exists():
            total_quantity = sum(item.quantity for item in qs)
            return total_quantity
        else:
            return 0
    else:
        return 0


