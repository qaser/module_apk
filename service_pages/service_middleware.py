from .models import Quote
import random


class QuoteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.quotes = [{'attrs': attr} for attr in Quote.objects.all()]

    def __call__(self, request):
        request.META['quote'] = random.choice(self.quotes)
        return self.get_response(request)
