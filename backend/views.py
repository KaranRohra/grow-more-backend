from django.http import JsonResponse


def index(request):
    return JsonResponse({"films": ["Dhoom 3", "Krish 3", "Bhootnath", "Koi mill gaya"]})
