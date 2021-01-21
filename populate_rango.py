import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'tango_with_django.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    
    # list of disctionary containing title and url of pages
    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/'},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/'},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/'} ]

    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/'},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/'} ]

    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask',
        'url':'http://flask.pocoo.org'}]

    # cats as in categories
    # pages values are the lists above
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }

    # categories and pages can be added using the list-dict formats above
    # iterates through cat list
    for cat, cat_data in cats.items():
        cat_views = cat_data['views']
        cat_likes = cat_data['likes']
        c = add_cat(cat, cat_views, cat_likes)
        # iterate through page list based of value of 'pages' of the category
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    # Print out the categories added
    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print(f'- {c}: {p}')

# add_page craetes a page under a certain category
# get_or_create(), save() is inherited from django.db.models
def add_page(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category = cat, title = title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

# creates a catagpry
def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name = name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


if __name__ == '__main__':
    print('Starting Rango population script')
    populate()



