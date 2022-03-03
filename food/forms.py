from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.forms import ModelForm
from .models import Food, Recipe, Ingredient, MealPlan, Member
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


# Widgets
class DateInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['user']


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'price', 'description', 'serving_size', 'unit',
                  'servings_per_container', 'calories', 'fat', 'carb', 'protein']


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'servings']


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['serving_amount']


class MealForm(ModelForm):
    class Meta:
        model = MealPlan
        fields = ['date', 'recipe', 'member', 'time']
        widgets = {
            'date': DateInput(),
            'time': TimePickerInput()
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
