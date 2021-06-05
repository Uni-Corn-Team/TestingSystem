from django.shortcuts import render


def handler404(request):
    template_name = '404.html'
    response = render(request, template_name)
    response.status_code = 404
    return response

