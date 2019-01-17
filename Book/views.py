from django.http import JsonResponse


def version(request):
    return JsonResponse({
        "data": "v0.0.1"
    })
