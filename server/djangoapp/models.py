from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Audi')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: {0}, Description: {1}".format(self.name, self.description)


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='Audi')
    dealership = models.IntegerField()
    TYPE_CHOICES = [
        ('SEDAN', 'SEDAN'),
        ('SUV', 'SUV'),
        ('MUV', 'MUV'),
        ('WAGON', 'WAGON'),
        ('COUPE', 'COUPE'),
        ('HATCHBACK', 'HATCHBACK'),
        ('MINIVAN', 'MINIVAN'),
    ]
    carType = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default='SEDAN'
    )
    year = models.DateField()

    def __str__(self):
        return "Name: {0}, Dealership: {1}, Type: {2}, Year: {3}".format(self.name, self.dealership, self.carType, self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, state, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.state = state
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, id, dealership, name, car_make, car_model, car_year, purchase, purchase_date, review, sentiment=None):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment
        self.time = now()

    def __str__(self):
        return "Review: " + self.review