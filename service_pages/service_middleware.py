from .models import Message, Quote
import random
from django.core.exceptions import ObjectDoesNotExist


class QuoteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.quotes = list(Quote.objects.all())

    def __call__(self, request):
        request.META['quote'] = random.choice(self.quotes)
        return self.get_response(request)


class MessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        try:
            self.last_message = Message.objects.latest('id')
        except ObjectDoesNotExist:
            self.last_message = None

    def __call__(self, request):
        request.META['last_message'] = self.last_message
        return self.get_response(request)
