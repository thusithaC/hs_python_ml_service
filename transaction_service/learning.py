
from django.http import HttpResponse, JsonResponse
from transaction_service.datasource import get_all_transactions

def test(request):
    return HttpResponse("Hello")

def transactions(request):
    return JsonResponse(get_all_transactions())
 