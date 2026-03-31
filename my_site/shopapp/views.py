import datetime
from timeit import default_timer

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

def shop_index(request: HttpRequest):
    products = [
        ("Laptop", 1999),
        ("Desctop", 2999),
        ("Smartphone", 999),
    ]
    context = {
        "date": datetime.datetime.now(),
        "time_running": default_timer(),
        "products": products,
    }
    return render(request, "shopapp/shop_index.html", context=context)