from .models import Control


class ControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.all_controls = Control.objects.all()

    def __call__(self, request):
        request.META['all_controls'] = self.all_controls
        return self.get_response(request)
