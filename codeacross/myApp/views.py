# from django.http import HttpResponse

# def index(request):
# 	return HttpResponse("my App Says Hello World")

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from myApp.models import Category, Page
from myApp.forms import CategoryForm

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
    context_dict = {'category_name': category_name}

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


# def about(request):
# 	return HttpResponse("myApp says This is About Page. <a href = '/myApp/'> Home</a>")

def about(request):
    # get the context from the request
    context = RequestContext(request)

    context_dict = { "boldmessage": "How I make a master of python django" }
    return render_to_response('myApp/about.html', context_dict, context)