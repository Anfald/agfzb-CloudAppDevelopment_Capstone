import requests
import json
# import related models here
import logging
from requests.auth import HTTPBasicAuth
from . import models
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


logger = logging.getLogger(__name__)
# Create a `get_request` to make HTTP GET requests
def get_request(url,**kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
    #    response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
       
        requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                   auth=HTTPBasicAuth('B5fDFSOU_ZA8xHOYMujpMFP_Aqnq1d6D69mNA_wTFlPg', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url,json_payload,**kwargs):
    response = requests.post(url, params=kwargs, json=payload)
    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
          #  dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = models.CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Perform a GET request with the specified dealer id
    json_result = get_request(url, dealerId = dealer_id)

    if json_result:
        # Get all review data from the response
        reviews = json_result["body"]["data"]["docs"]
        # For each review in the response
        for review in reviews:
            # Create a DealerReview object from the data
            review_content = review["review"]
            id = review["_id"]
            name = review["name"]
            purchase = review["purchase"]
            dealership = review["dealerships"]

            try:
                # These values may be missing
                car_make = review["car_make"]
                car_model = review["car_model"]
                car_year = review["car_year"]
                purchase_date = review["purchase_date"]

                # Create a review object with values in 'doc' object
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase, 
                    review=review_content, car_make=car_make, car_model=car_model, 
                    car_year=car_year, purchase_date=purchase_date
                    )
            except KeyError:
                print("Something missing from this review. Using default values.")
                # Create review object with default values
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase,
                    review=review_content
                    )
            # Analyze sentiment of the review text and save it to sentiment attribute
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print("sentiment: {review_obj.sentiment}")

            # Save review object to the list result
            results.append(review_obj)

    return results
###########
#def get_dealer_reviews_from_cf(url, dealerId):
#    results = []
 #   # Call get_request with a URL parameter
  #  json_result = get_request(url , dealerId=dealerId)
  #  if json_result:
        # Get the row list in JSON as dealers
   #      reviews = json_result['entries']
    #     for review in reviews:
     #        try:
      #          review_obj = models.DealerReview(name = review["name"], 
       #         dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
        #        purchase_date = review["purchase_date"], car_make = review['car_make'],
        #        car_model = review['car_model'], car_year= review['car_year'], sentiment= "none")
        #     except:
         #       review_obj = models.DealerReview(name = review["name"], 
         #       dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
         #       purchase_date = 'none', car_make = 'none',
          #      car_model = 'none', car_year= 'none', sentiment= "none")
                
         #   review_obj.sentiment = analyze_review_sentiments(review_obj.review)
          #  print(review_obj.sentiment)
                    
         #   results.append(review_obj)

 #   return results

def get_dealer_by_id(url, dealer_id):
    # Call get_request with the dealer_id param
    json_result = get_request(url,dealer_id=dealer_id)
    print(json_result)
    # Create a CarDealer object from response
    dealer = json_result["entries"]
    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                           id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                           short_name=dealer["short_name"],
                           st=dealer["st"], zip=dealer["zip"])

    return dealer_obj


# Gets all dealers in the specified state from the Cloudant DB with the Cloud Function get-dealerships
def get_dealers_by_state(url, state):
    results = []
    # Call get_request with the state param
    json_result = get_request(url, state=state)
    dealers = json_result["body"]["docs"]
    # For each dealer in the response
    for dealer in dealers:
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], zip=dealer["zip"])
        results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
   # get_request(url,**kwargs)
    api_key = "B5fDFSOU_ZA8xHOYMujpMFP_Aqnq1d6D69mNA_wTFlPg"
    url = "https://cc248213-edab-40c2-b84b-e84c1536c6c6-bluemix.cloudantnosqldb.appdomain.cloud"
    texttoanalyze= text
    version = '20000'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='222222',
    authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=text,
        features= Features(sentiment= SentimentOptions())
    ).get_result()
    print(json.dumps(response))
    sentiment_score = str(response["sentiment"]["document"]["score"])
    sentiment_label = response["sentiment"]["document"]["label"]
    print(sentiment_score)
    print(sentiment_label)
    sentimentresult = sentiment_label
    
    return sentimentresult
