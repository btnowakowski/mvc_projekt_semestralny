from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Admin").exists()


admin_required = user_passes_test(is_admin)
