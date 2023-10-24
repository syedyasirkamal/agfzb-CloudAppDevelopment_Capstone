from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json 

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
#def index(request):
#    context = {}
#    return render(request, 'djangoapp/index.html', context)


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
             # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.error("New user")
        # If it is a new user
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to index page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "/get-dealership"
        # Get dealers from the URL

        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = {
            "dealerships": get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        d_url = f"/get-dealership?id={dealer_id}"
        r_url = f"/get-review?id={dealer_id}"
        # Get dealers from the URL
        context = {
            "dealer": get_dealer_by_id_from_cf(d_url),
            "reviews": get_dealer_reviews_from_cf(r_url),
        }
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review

def add_review(request, dealer_id):
    if request.user.is_authenticated:
        context = {}
        d_url = f"/get-dealership?id={dealer_id}"
        if request.method == "GET":
            context = {
            "cars": CarModel.objects.all(),
            "dealer": get_dealer_by_id_from_cf(d_url)
        }
            return render(request, 'djangoapp/add_review.html', context)
        
        if request.method == "POST":
            if request.user.is_authenticated:
                username = request.user.username
                print(request.POST)
                form = request.POST 
                payload = dict()
                car_id = form.get("car")
                car = CarModel.objects.get(pk=car_id)
                print(car)
                payload["name"] = username
                payload["dealership"] = dealer_id
                payload["id"] = dealer_id
                payload["review"] = form.get("review")
                payload["purchase"] = False
                if "purchasecheck" in request.POST:
                    if request.POST["purchasecheck"] == 'on':
                        payload["purchase"] = True
                payload["purchase_date"] = form.get("purchase_date")
                payload["car_make"] = car.make.name
                payload["car_model"] = car.name
                payload["car_year"] = int(car.year)
                new_payload = {}
                new_payload["review"] = payload
                r_url = f"https://us-east.functions.appdomain.cloud/api/v1/web/a797e456-523c-46b4-88e1-60e11636e7d5/dealership-package/post-reviews?id={dealer_id}"
                post_request(r_url, new_payload, id=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        return redirect("/djangoapp/login")

