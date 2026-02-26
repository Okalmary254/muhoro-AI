from django.urls import path
from django.http import JsonResponse
from .views import translate_api, home

urlpatterns = [
    path("translate/", translate_api),
    path("", home)
]

def api_root(request):
    return JsonResponse({
        "translate": "/api/translate/"
    })