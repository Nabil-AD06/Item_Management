from django.shortcuts import render
from django.http import HttpResponse
 
def _sayHello(request): 
    return HttpResponse("hello")
