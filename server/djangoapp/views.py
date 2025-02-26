from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_request, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
   context = {}
   if request.method == 'GET':
      return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    #  POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp/')
        else:
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    # Redirect user back to carlist view
    return redirect ('/djangoapp')       
                  #('djangoapp:index') to redirect to main page but /djangoapp is better

# Create a `registration_request` view to handle sign up request
def registration_request(request):
     context = {}
     # from the course (Developing Applications with SQL, Databases, and Django) I see like this method              
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
       return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("/djangoapp/")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# here  needs to 
def get_dealerships(request):
    #context = {}
    # if request.method == "GET":
    #    return render(request, 'djangoapp/index.html', context)
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/Anfald_dev/dealership-package/get-dealership.json" # here update
        context = {"dealerships": restapis.get_dealers_from_cf(url)}
        # Get dealers from the URL
       # dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
       # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
     context = {}
    if request.method == "GET":
        url = 'https://eu-gb.functions.appdomain.cloud/api/v1/web/Anfald_dev/dealership-package/get-review?id=15'     ### ubdate see ?id=15
       # context = {"reviews":  restapis.get_dealer_reviews_by_id_from_cf(url, dealer_id)}
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = {
            "reviews": reviews,
            "dealer_id": dealer_id,
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # Verify the user is authenticated
    if request.user.is_authenticated:
        # GET request renders the page with the form for filling out a review
        if request.method == "GET":
            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/Anfald_dev/dealership-package/get-dealership?id=dealer_id"   ### here the end i edit 
            # Get dealer details from the API
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id(url, dealer_id=dealer_id),
            }
            return render(request, 'djangoapp/add_review.html', context)
        # POST request posts the content in the review submission form to the Cloudant DB using the post_review Cloud Function
        if request.method == "POST":
            form = request.POST
            review = dict()
            review["name"] = "{request.user.first_name} {request.user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            if review["purchase"]:
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%d/%m/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year

            # If the user bought the car, get the purchase date
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%d/%m/%Y").isoformat()
            else:
                review["purchase_date"] = None

            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/Anfald_dev/dealership-package/post-review"
            json_payload = {"review": review}
            result = post_request(url, json_payload, dealerId=dealer_id)
            if int(result.status_code) == 200:
                print("Review posted successfully.")

            # After posting the review the user is redirected back to the dealer details page
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

        else:
            # If user isn't logged in, redirect to login page
            print("Please login in to post a review")
            return redirect("/djangoapp/login")

