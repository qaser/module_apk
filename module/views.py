from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index_page(request):
    return render(request, 'module/main-menu.html',)
