from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    # context_dict = {"boldmessage":"Crunchy, creamy, cookie, candy, cupcake!"}
    # return render(request, 'rango/index.html', context=context_dict)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = "Crunchy, creamy, cookie, candy, cupcake!"
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    visitor_cookie_handler(request)
    response = render(request, 'rango/index.html', context=context_dict)

    return response

def about(request):
    context_dict = {"boldmessage":"This tutorial has been put together by Yu Kit"}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, "rango/about.html", context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    # a http post - sends data to the server
    if request.method == 'POST':
        form = CategoryForm(request.POST)

    if form.is_valid():
        form.save(commit = True)
        return redirect('/rango')
    else:
        print(form.errors)
    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category == None:
        return redirect('/rango/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                    kwargs={'category_name_slug':category_name_slug}))

        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid and profile_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {'user_form':user_form, 'profile_form': profile_form, 'registered':registered}
    return render(request,'rango/register.html',context=context)


def user_login(request):
    # if request is post, try to obtain relevant information
    if request.method == 'POST':
        # use .get instead of just POST because .get returns an error instead of a keyerror exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        # if there is a user object username and password are correct
        if user:
            # checks if it is not disabled
            # if active, log user in and send back to index page
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            # dont log in if disabled
            else:
                return HttpResponse("Your Rango account is disabled.")
        # bad details were provided so dont login
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    # this scenario is most likely a http get, meaning that it is asking to login, need to create templatye login.html
    else:
        return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


# track number of times accessed helper function
def visitor_cookie_handler(request):
    # if cookie exists, it will return the value of the cookie
    # else, it reutrns value 1 and sets value of visits in the cookie to be 1
    visits = int(get_server_side_cookie(request,'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

# checks if last visit was more than one day ago
# if more than a day ago, increm3ent visits by 1 and sets the last visit to current time
# else dont increment and sets the last visit cookie to itself
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
