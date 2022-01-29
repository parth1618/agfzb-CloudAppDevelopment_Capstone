from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, reverse
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

BASE_URL = "https://a06c0516.eu-gb.apigw.appdomain.cloud/api/{0}"


# Create your views here.
def index(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            logger.info("User logged in: `{}`".format(username))
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            logger.error("Error while logging in.")
            context['message'] = "Invalid UserName or Password"
            return render(request, 'djangoapp/login.html', context)
    else:
        logger.error("Log In: Invalid Request")
        context['message'] = "Invalid Request"
        return render(request, 'onlinecourse/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logger.info("Log out the user `{}`".format(request.user.username))
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
            return redirect("djangoapp:index")
        else:
            context['message'] = 'User Exists.'
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(BASE_URL.format('dealership'))
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(BASE_URL.format('review'), dealer_id)
        dealer = get_dealer_by_id_from_cf(BASE_URL.format('dealership'), dealer_id)
        
        context['review_list'] = reviews
        context['dealer'] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    import uuid
    if request.method == "GET":
        context = {}
    
        dealer = get_dealer_by_id_from_cf(BASE_URL.format('dealership'), dealer_id)
        context['dealer'] = dealer
        
        cars = CarModel.objects.all().filter(dealership=dealer_id)
        if cars:
            context['cars'] = cars

        return render(request, 'djangoapp/add_review.html', context)
    
    elif request.method == "POST":
        
        postData = {}
        postData["id"] = 11
        postData["dealership"] = dealer_id
        postData["name"] = request.user.username

        car = get_object_or_404(Course, pk=request.POST["car"]) if request.POST.get("car", None) else None
        if car:
            postData["car_make"] = str(car.carMake.name) if car else "NA"
            postData["car_model"] = str(car.name) if car else "NA"
            postData["car_year"] = car.year.strftime("%Y") if car else "NA"
        if request.POST.get("purchasecheck", None):
            postData["purchase"] = request.POST.get("purchasecheck", False)
        
        if request.POST.get("purchasedate", None):
            postData["purchase_date"] = request.POST.get("purchasedate", None)
        
        postData["review"] = request.POST.get("content", "")

        response = post_request(BASE_URL.format('review'), postData)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        pass

