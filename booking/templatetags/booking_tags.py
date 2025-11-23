from django import template
from booking.utils.permissions import is_admin as is_admin_check

register = template.Library()


@register.filter
def is_admin(user):
    return is_admin_check(user)
