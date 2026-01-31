from django.urls import path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ecpay_callback(request):
    if request.method == 'POST':
        # TODO: Implement signature verification and status update
        print("ECPay Callback:", request.POST)
        return HttpResponse('1|OK')
    return HttpResponse('Method Not Allowed', status=405)

urlpatterns = [
    path('callback/ecpay/', ecpay_callback, name='ecpay_callback'),
]
