import requests
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

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
def post_request(url, jsonPayload, **kwargs):
    json_payload = json.loads(jsonPayload)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=json_payload, headers=headers, params=kwargs, timeout=10)
    return response.json()


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

    # Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealer_details_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_by_id_from_cf(url):
    json_result = get_request(url)
    if json_result:
        dealer_doc = json_result[0]
        print(dealer_doc)
        print(json_result)
        dealer_obj = CarDealer(
            address=dealer_doc["address"],
            city=dealer_doc["city"],
            full_name=dealer_doc["full_name"],
            id=dealer_doc["id"],
            lat=dealer_doc["lat"],
            long=dealer_doc["long"],
            short_name=dealer_doc["short_name"],
            st=dealer_doc["st"],
            zip=dealer_doc["zip"]
        )
    return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["data"]
        # For each dealer object
        for review_doc in reviews["docs"]:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                sentiment=analyze_review_sentiments(review_doc["review"])
            )
            results.append(review_obj)
    return results


def analyze_review_sentiments(text):
    url="https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/87f40213-fd55-4c4e-9f13-ac79c9aa1b13"
    api_key="a-L5AE4oo8-oI9x2fLcNLdT660aLALfRb-Cdojj64BJ4"
    texttoanalyze=text
    version='2020-08-01'
    authenticator=IAMAuthenticator(api_key)
    natural_language_understanding=NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=text,
        features= Features(sentiment= SentimentOptions()),
        language="en"
    ).get_result()
    print(json.dumps(response))
    sentiment_score = str(response["sentiment"]["document"]["score"])
    sentiment_label = response["sentiment"]["document"]["label"]
    print(sentiment_score)
    print(sentiment_label)
    sentimentresult = sentiment_label
    
    return sentimentresult