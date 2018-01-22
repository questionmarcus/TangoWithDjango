# Copied from page 55-56 of "Tango with Django"

import os
import django
from rango.models import Category, Page

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')
django.setup()

def populate():
    '''
    First we will create lists of dictionaries containing the pages we want
    to add in each category. Then we will create a dictionary of directories
    for our catagories. This might seem a bit confusing, but it allows us
    to iterate through each data structure, and add the data to our models
    '''

    python_pages = [
            {"title": "Official Python Tutorial",
                "url": "https://docs.python.org/3/tutorial" }
            {"title": "How to Think Like a Computer Scientist",
                "url": "https://www.greenteapress.com/thinkpython"}
            {"title": "Learn Python in 10 Minutes",
                "url": "https://www.korokithakis.net/tutorials/python"}
            ]

    django_pages = [
            {"title": "Official Django Tutorial",
                "url": "https://docs.djangoproject.com/en/2.0"}
            {"title": "Django Rocks",
                "url": "https://www.djangorocks.com"}
            {"title": "How to Tango with Django",
                "url": "https://www.tangowithdjango.com/"}
            ]

    other_pages = [
            {"title": "Bottle",
                "url": "http://bottlepy.org/docs/dev/"}
            {"title": "Flask",
                "url": "http://flask.pocoo.org/"}
            ]

    cats = {"Python": {"pages": python_pages},
            "Django": {"pages": django_pages},
            "Other Frameworks": {"pages": other_pages}}

    # If you want to add more categories or pages, add them to the dictionaries
    # above.
    #
    # The code below goes through the cat dictionary, then adds each catagory,
    # then adds all the associated pages for that catagory.

    for cat, cat_data in cat.items():
        c = add_cat(cat)
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"])

    # Print our categories we have added
    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category = cat, title = title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name = name)[0]
    c.save()
    return c

if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()

