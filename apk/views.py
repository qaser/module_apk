from apk.models import Fault
from django.shortcuts import render


def index(request):
    faults = Fault.objects.all()
    return render(
        request,
        'apk/index.html',
        {'faults': faults},
    )