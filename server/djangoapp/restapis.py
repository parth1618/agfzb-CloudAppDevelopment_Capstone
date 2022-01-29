import requests
import json
from models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, json=payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:

        # Here we can add further refinement to handle 404 and 500
        if json_result["code"] != 200:
            return results

        dealers = json_result["response"]
        # For each dealer object
        for dealer_doc in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:

        # Here we can add further refinement to handle 404 and 500
        if json_result["code"] != 200:
            return results

        dealers = json_result["response"]
        # For each dealer object
        for dealer_doc in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_by_id_from_cf(url, dealerId):
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:

        # Here we can add further refinement to handle 404 and 500
        if json_result["code"] != 200:
            return results

        dealer_doc = json_result["response"]
        
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:

        # Here we can add further refinement to handle 404 and 500
        if json_result["code"] != 200:
            return results

        reviews = json_result["response"]
        # For each dealer object
        for review_doc in reviews:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(id=review_doc["id"], dealership=review_doc["dealership"], name=review_doc.get("name", ""), car_make=review_doc.get("car_make", "NA"),
                                   car_model=review_doc.get("car_model", "NA"), car_year=review_doc.get("car_year", "NA"), purchase=review_doc.get("purchase", False),
                                   purchase_date=review_doc.get("purchase_date", "NA"), review=review_doc.get("review", ""))
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    try:
        API_KEY = "K02lvdx_9fpGddEFYpOTk1iLDT7c0ZBJQyPb3VD1rUdc"
        URL = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/81d0cec9-21fc-458d-8c90-82a6ffda8aee"

        authenticator = IAMAuthenticator(API_KEY)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=authenticator
            )

        natural_language_understanding.set_service_url(URL)

        response = natural_language_understanding.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()

        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        
        label = response['sentiment']['document']['label'] 

        return label
    except:
        # If any error occurs
        print("Network exception occurred")


