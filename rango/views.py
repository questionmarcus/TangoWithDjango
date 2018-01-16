from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says \"Hey there, partner!\"")

def about(request):
    return HttpResponse(
        "Rango says \"Here is the about page\". "+
        "<a href='/rango/'>Back Home</a>"
    )
