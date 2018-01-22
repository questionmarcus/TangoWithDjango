# Copied from page 55-56 of "Tango with Django"

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    '''
    First we will create lists of dictionaries containing the pages we want
    to add in each category. Then we will create a dictionary of directories
    for our catagories. This might seem a bit confusing, but it allows us
    to iterate through each data structure, and add the data to our models
    '''

    python_pages = [
            {"title": "Official Python Tutorial",
                "url": "https://docs.python.org/3/tutorial" ,
                "views": 10},
            {"title": "How to Think Like a Computer Scientist",
                "url": "https://www.greenteapress.com/thinkpython",
                "views": 42},
            {"title": "Learn Python in 10 Minutes",
                "url": "https://www.korokithakis.net/tutorials/python",
                "views": 21}
            ]

    django_pages = [
            {"title": "Official Django Tutorial",
                "url": "https://docs.djangoproject.com/en/2.0",
                "views": 32},
            {"title": "Django Rocks",
                "url": "https://www.djangorocks.com",
                "views": 14},
            {"title": "How to Tango with Django",
                "url": "https://www.tangowithdjango.com/",
                "views": 20}
            ]

    other_pages = [
            {"title": "Bottle",
                "url": "http://bottlepy.org/docs/dev/",
                "views": 39},
            {"title": "Flask",
                "url": "http://flask.pocoo.org/",
                "views": 50}
            ]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}}

    # If you want to add more categories or pages, add them to the dictionaries
    # above.
    #
    # The code below goes through the cat dictionary, then adds each catagory,
    # then adds all the associated pages for that catagory.

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

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

def add_cat(name, v=0, l=0):
    c = Category.objects.get_or_create(name = name, views = v, likes = l)[0]
    c.save()
    return c

if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()

