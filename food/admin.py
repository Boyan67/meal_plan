from django.contrib import admin
from .models import Member, Food, Recipe, Ingredient, MealPlan
# Register your models here.
admin.site.register(Member)
admin.site.register(Food)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(MealPlan)
