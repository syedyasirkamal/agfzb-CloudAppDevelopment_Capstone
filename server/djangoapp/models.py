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


# <HINT> Create a plain Python class `DealerReview` to hold review data
