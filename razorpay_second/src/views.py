from django.shortcuts import render
import razorpay
from . models import *
# Create your views here.

def home(request):
    if request.method == "POST":
        name=request.POST.get("name")
        amount=int(request.POST.get("amount") )* 100
        client = razorpay.Client(auth=("rzp_live_oFFQJco5Abpnjc","AZTrtfaqmpQ04xHVocIRCFQf"))
        payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        print(payment)
        coffee=Coffee(name=name, amount=amount, payment_id=payment['id'])
        coffee.save()

        return render(request,'index.html',{'payment':payment})

    return render(request,'index.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        payment_id = ""
        for key, val in a.items():
            payment_id = val
            break
        user = Coffee.objects.filter(payment_id=payment_id).first()
        if user:
            user.paid = True
            user.save()
        print(a)
    return render(request, 'success.html')