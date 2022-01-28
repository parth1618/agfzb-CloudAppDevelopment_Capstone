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


# <HINT> Create a plain Python class `DealerReview` to hold review data
