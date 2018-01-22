from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    # Construct a dict to pass to the template engine
    # This dict tell the template what value should be placed in
    # {{ boldmessage }}

    # Return a rendered response to send to the client
    # render function takes a request, the template filename and the context
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!",
            'categories': category_list,
            'pages': page_list}

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')
#    return HttpResponse(
#        "Rango says \"Here is the about page\". "+
#        "<a href='/rango/'>Back Home</a>"
#    )

def show_category(request, category_name_slug):
    # Create a context dictionary to pass to the template rendering engine
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)
