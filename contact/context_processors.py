from django.conf import settings


def add_settings(request):
    """
        Adding project settings to the context.
    """
    return {'project_settings': settings}