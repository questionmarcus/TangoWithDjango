from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime

def index(request):
    # Construct a dict to pass to the template engine
    # This dict tell the template what value should be placed in
    # {{ boldmessage }}

    # Return a rendered response to send to the client
    # render function takes a request, the template filename and the context

    request.session.set_test_cookie() # Cookie test
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!",
            'categories': category_list,
            'pages': page_list}

    # update cookie information
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # get response object earlier so we can add cookies to it
    response = render(request, 'rango/index.html', context=context_dict)
    return response

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    visitor_cookie_handler(request)

    context_dict = {'visits': request.session['visits']}
    return render(request, 'rango/about.html', context_dict)

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

@login_required
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

@login_required
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
            user_form = UserForm()
            profile_form = UserProfileForm()

    return render(
            request,
            'rango/register.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered}
            )

def user_login(request):
    # If request is a post (completed the form)
    if request.method == 'POST':
        # gather relevant information from the request
        # use request.POST.get so that if the information is
        # missing, it will return "None" rather than raise an error
        username = request.POST.get("username")
        password = request.POST.get("password")

        # use Django to test is the user details are correct
        user = authenticate(username=username, password=password)

        if user:
            # if the account is active
            if user.is_active:
                # log the user in and send them to the main page
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # If the account was deactivated, don't log them in
                return HttpResponse("Your rango account is disabled")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # If a HTTP Get request was made, display the login details
    else:
        return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    # As we are using the login_required decorator, we know we dont have to
    # test for the user being logged in
    logout(request) # Log the user out
    # Now they are logged out, send them back to the homepage
    return HttpResponseRedirect(reverse("index"))

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
