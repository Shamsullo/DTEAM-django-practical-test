from django.conf import settings


def settings_context(request):
    """Context processor that provides Django settings to all templates."""
    return {"settings": settings}
