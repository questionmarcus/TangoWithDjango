from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Construct a dict to pass to the template engine
    # This dict tell the template what value should be placed in
    # {{ boldmessage }}

    # Return a rendered response to send to the client
    # render function takes a request, the template filename and the context
    context_dict = {'boldmessage': "The Ting Goes Skraaaa"}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return HttpResponse(
        "Rango says \"Here is the about page\". "+
        "<a href='/rango/'>Back Home</a>"
    )
