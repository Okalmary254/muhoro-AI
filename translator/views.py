from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.engine import translate_text
from django.shortcuts import render


def home(request):
    return render(request, "translator/index.html")

@api_view(["POST"])
def translate_api(request):
    text = request.data.get("text")
    target = request.data.get("target", "eng_Latn")

    if not text:
        return Response({"error": "Text required"}, status=400)

    try:
        result = translate_text(text, target)
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=500)