from .models import Control, Role


class ApkMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.all_controls = Control.objects.all()
        self.roles = Role.__members__

    def __call__(self, request):
        request.META['all_controls'] = self.all_controls
        request.META['roles'] = self.roles
        return self.get_response(request)
