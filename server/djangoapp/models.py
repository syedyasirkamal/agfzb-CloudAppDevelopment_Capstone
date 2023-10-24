from django.db import models


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name =  models.CharField(null=False, max_length=20, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return f"Name: {self.name} \nDescription: {self.description}" 


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_name = models.CharField(null=False, max_length=20, primary_key=True)
    dealer_id = models.IntegerField(null=False)
    car_model = models.CharField(max_length=15, choices=(('SEDAN', 'Sedan'),('SUV', 'SUV'),('WAGON', 'Wagon')))
    car_year = models.DateField()

    def __str__(self):
        return f"Name: {self.car_name} | Model Type: {self.car_model} | Make: {self.car_make} \nYear: {self.car_year}\nDealer ID: {self.dealer_id}"


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

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, name, dealership, review, purchase, sentiment=None, purchase_date=None, car_make=None, 
                    car_model=None, car_year=None):
        # Dealership
        self.dealership = dealership
        # Dealership name
        self.name = name
        # Dealership purchase | Boolean
        self.purchase = purchase
        # Review
        self.review = review
        # Purchase Date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model 
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # Sentiment of the review
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review