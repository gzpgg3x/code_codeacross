# from django.http import HttpResponse

# def index(request):
# 	return HttpResponse("my App Says Hello World")

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from myApp.models import Category, Page
from myApp.forms import CategoryForm, PageForm
from myApp.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login

# def encoding(category_name_url):
#     category_name = category_name_url.replace('_', ' ')
#     return category_name
def encode_url(str):
    return str.replace(' ', '_')

# def decoding(category_name):
#     category_name_url = category_name.replace(' ', '_')
#     return category_name_url
def decode_url(str):
    return str.replace('_', ' ')    

# def index(request):
#     return HttpResponse("myApp says hello world! <a href = '/myApp/about'>about</a>")
#     # return HttpResponse("myApp says hello world! about <a ref = '/myApp/about'>about</a>") 

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as  {{ boldmessage }} in the template!
    # context_dict = { "boldmessage": "I must learn python django line by line by heart" }

    # Query the database for a list of All categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    # category_list = Category.objects.order_by(views:-5) 
    # category_list = Category.objects.order_by(-views)[:5]
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # context_dict = {'categories': category_list}
    context_dict = {'categories': category_list, 'pages': page_list}

    # for category in categories:
    #     category_name_url = category_name.replace(" ", "_")
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e. g. spaces replaced with underscores).
    for category in category_list:
        # category_name_url =  category.name.replace(" ", "_")
        # category.url = category.name.replace(" ", "_")
        category.url = encode_url(category.name)

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('myApp/index.html', context_dict, context)

def category(request, category_name_url):
    # Request our context from the request passed to us.
    # context = ContextRequest(request)
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    # category_name = category_name_url.replace('_', ' ')
    category_name = decode_url(category_name_url) 


    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    # context_dict = {'pages': page_list}
    # context_dict = {'category_name': category_name}
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        # category = Category.objects.get(category_name)
        category = Category.objects.get(name = category_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >=1 model instance.
        # page = Category.ojbects.filter(category = category)
        pages = Page.objects.filter(category = category)

        # Add our results list to the template context under name pages.
        # context_dict['page'] = pages 
        context_dict['pages'] = pages 
        # We also add the category object from the database to the context dictionary
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] =  category
    except Category.DoesNotExist:
        # We get here if we didn't find the spcified category.
        # Don't do anything - the template displays the "no category " message for us.
        pass 

    # Go render the response and return it to the client.
    return render_to_response('myApp/category.html', context_dict, context)

def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Nwo call the index() view.
            # The user will be shown the homepage.
            return index(request)

        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied    
    # Render the form with error messages (if any).
    # context_dict = 
    return render_to_response('myApp/add_category.html', {'form': form}, context)

# def add_page(request):
def add_page(request, category_name_url):
    # context = ContextRequest(request)
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # form.save(commit=True)
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # REtrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category from as a way of saying the category does not esixt.
                # return render_to_response('myApp/add_page.html', {'form': form}, context)
                return render_to_response('myApp/add_category.html', {}, context)

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else: 
            print form.error

    else:
        form = PageForm()

    # return render_to_response('myApp/add_page', {'form': form}, context)
    return render_to_response('myApp/add_page.html', {'form': form, 'category_name_url': category_name_url, 'category_name': category_name}, context)


# def about(request):
# 	return HttpResponse("myApp says This is About Page. <a href = '/myApp/'> Home</a>")

def about(request):
    # get the context from the request
    context = RequestContext(request)

    context_dict = { "boldmessage": "How I make a master of python django" }
    return render_to_response('myApp/about.html', context_dict, context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the tmeplate whether the registration  was successful.
    registered = False

    # context_dict = ()

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # user_form.save(commit=True)
            # profile_form.save(commit=True)
            user.set_password(user.password)
            # user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=false.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True                

        # Invalid form or forms - mistake or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            # The supplied form contained errors - just print them to the terminal.
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.        
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response('myApp/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered':registered}, context)

def user_login(request):
    # Like before, obtain the context for the user's request. 
    context = RequestContext(request)

    # If the request is s a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the Login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # Is the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/myApp/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login detials: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely to a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('myApp/login.html', {}, context)