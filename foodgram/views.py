from django.shortcuts import render


def page_bad_request(request, exception):
    return render(
        request, 'error/400.html', {'path': request.path}, status=400
    )


def page_not_found(request, exception):
    return render(
        request, 'error/404.html', {'path': request.path}, status=404
    )


def server_error(request):
    return render(request, 'error/500.html', status=500)
