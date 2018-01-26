from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

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

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # if entered for is valid, add it to the database
            form.save(commit=True)
            # now send the user back to the homepage
            return index(request)
        else:
            # if form has errors, show them to the user
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # Value to store whether the user registered correctly
    registered = False

    # If it is a POST request, we can process the data
    if request.method == 'POST':
        # Grab data from the information sent from the form in the POST request
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # save the form data to the database
            user = user_form.save()

            # Hash the password using the set_password method
            user.set_password(user.password)
            # update the user object
            user.save()

            # Since we have to set the user attributes for UserProfiles ourself
            # we set commit to false to delay saving it to the database.
            # This avoids integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # if the user uploaded a picture, add it to the model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # we can now save the profile model
            profile.save()

            # we have now registered!
            registered = True
        else:
            print(user_forms.errors, profile_forms.errors)
    else:
            # if it is not a POST request, the forms will be blank awaiting input
            user_form = UserForm
            profile_form = UserProfileForm()

    return render(
            request,
            'rango/register.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered}
            )
