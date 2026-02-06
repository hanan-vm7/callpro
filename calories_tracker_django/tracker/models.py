from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=50,null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    password=models.CharField(max_length=15,null=True,blank=True)
    calorie_goal=models.IntegerField(null=True,blank=True)
    protein_goal=models.IntegerField(null=True,blank=True)
    image=models.ImageField(upload_to="profile_image/",null=True,blank=True)
    

from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True )
    calories = models.IntegerField()
    protein = models.FloatField()
    fav=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

from django.conf import settings
from .models import User

class MealLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    food_name = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField()
    total_calories = models.IntegerField()
    total_protein = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.food.name} - {self.user.username}"
    def get_food_name(self):
        return self.food.name if self.food else self.food_name
    
class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    custom_name = models.CharField(max_length=100, null=True, blank=True)
    calories = models.IntegerField()
    protein = models.FloatField()
    
    def __str__(self):
        return self.custom_name or self.food.name


    
