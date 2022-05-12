from PIL import Image
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default='aaa.jpg', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile_pic.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.profile_pic.path)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    serving_size = models.IntegerField(null=True)
    unit = models.CharField(max_length=200, null=True)
    servings_per_container = models.FloatField(null=True)
    calories = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    carb = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    price_per_serving = models.FloatField(null=True)
    price_per_100cal = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, null=True)
    calories = models.FloatField(null=True)
    servings = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    carb = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    price_per_serving = models.FloatField(null=True)
    price_per_100cal = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    serving_amount = models.FloatField(null=True)
    unit = models.CharField(max_length=200, null=True)
    calories = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    carb = models.FloatField(null=True)
    protein = models.FloatField(null=True)

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    date = models.DateField()
    day = models.CharField(max_length=10, default=' ', null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return self.date.__str__() + " - " + self.recipe.name
