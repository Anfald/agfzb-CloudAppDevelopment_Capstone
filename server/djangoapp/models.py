from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model

class CarMake(models.Model):
    name = models.CharField(null= False, max_length=30, default='car model')
    desc = models.CharField(null= False, max_length=200, default='car description ')
    
# - __str__ method to print a car make object
    def __str__(self):     
       # return self.name
        return 'Name:' + self.name + ',' + \
            'Description:' + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
class CarModel(models.Model):
    carmake = models.ForeignKey(CarMake, null= True, on_delete=models.CASCADE)
    name = models.CharField(null= False, max_length=30, default='car name')
    dealerid = models.IntegerField(null=True)
    year = models.DateField(null= True)
# - __str__ method to print a car make object
    def __str__(self):
        return 'Name ' + self.name



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
        self.idx = 0

    def __str__(self):
        return "Dealer name: " + self.full_name
 # <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, id, review, sentiment, **kwargs):
        
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.id = id
        self.review = review
        self.sentiment = sentiment
        
        if purchase:
            self.purchase_date = kwargs["purchase_date"]
            self.car_make = kwargs["car_make"]
            self.car_model = kwargs["car_model"]
            self.car_year = kwargs["car_year"]
        
        
    def __str__(self):
        return "Review: " + self.review
############
# <HINT> Create a plain Python class `DealerReview` to hold review data
#class DealerReview:
 #   def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment):
  #      # Dealership
  #      self.dealership = dealership
        # Dealer name
  #     self.name = name
        # Dealer purchase
    #    self.purchase = purchase
        # Dealer review
     #   self.review = review
        # purchase_date
   #     self.purchase_date = purchase_date
        # car_make
   #     self.car_make = car_make
        # car_model
   #     self.car_model = car_model
        # car_year
   #     self.car_year = car_year
        # sentiment
   #     self.sentiment = sentiment
        # id
       # self.id = id

   # def __str__(self):
   #     return  "Review: " + self.review
########
