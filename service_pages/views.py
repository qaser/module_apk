from django.shortcuts import render
# from django.views.generic.base import TemplateView

# class AboutView(TemplateView):
#     template_name = 'service_pages/author.html'


# class DocView(TemplateView):
#     template_name = 'service_pages/tech.html'


# class HelpView(TemplateView):
#     template_name = 'service_pages/tech.html'


def page_not_found(request, exception):
    return render(
        request,
        'service_pages/errors/404.html',
        {'path': request.path}, status=404
    )


def server_error(request):
    return render(request, 'service_pages/errors/500.html', status=500)


def bad_request(request, exception):
    return render(
        request,
        'service_pages/errors/400.html',
        {'path': request.path}, status=400
    )
