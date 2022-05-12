import re

from django.contrib.auth import authenticate, logout, login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Food, Recipe, Ingredient, MealPlan, Member
from .forms import FoodForm, RecipeForm, IngredientForm, MealForm, CreateUserForm, MemberForm
import datetime
from collections import Counter
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def profile(request):
    member = request.user.member
    form = MemberForm(instance=member)

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'food/account/profile.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()

                messages.success(request, 'Account was created for ' + user.username)
                Member.objects.create(user=user, name=user.username, email=user.email)

                return redirect('login')

        context = {'form': form}
        return render(request, 'food/account/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'food/account/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


# Create your views here.
@login_required(login_url='login')
def home(request):
    meal_plans = MealPlan.objects.order_by('date')
    ingredient_list = []
    for i in meal_plans:
        i.day = i.date.strftime("%A").upper()
        i.save()
        meal_ingredients = (Ingredient.objects.all().filter(recipe=i.recipe))
        for j in meal_ingredients:
            ingredient_list.append(j)

    count_dict = dict(Counter(ingredient_list).items())
    for key, value in count_dict.items():
        count_dict[key] = value * key.serving_amount

    context = {'meal_plans': meal_plans, 'ingredient_list': ingredient_list, 'count_dict': count_dict}
    return render(request, 'food/dashboard.html', context)


# ============
# Meal Plans
# ============
@login_required(login_url='login')
def add_meal(request):
    form = MealForm()
    context = {'form': form}
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, message='You have entered an invalid date')
    return render(request, "food/meal/add_meal.html", context=context)


@login_required(login_url='login')
def delete_meal(request, pk):
    meal = MealPlan.objects.get(id=pk)
    context = {'meal': meal}
    if request.method == "POST":
        meal.delete()
        return redirect('home')
    return render(request, 'food/meal/delete_meal.html', context)


@login_required(login_url='login')
def generate_shopping(request):
    meals = MealPlan.objects.all()
    ingredient_list = []
    for i in meals:
        ingredient_list.append(Ingredient.objects.filter(recipe=i.recipe))

    context = {'ingredient_list': ingredient_list}
    return render(request, 'food/dashboard.html', context)


# ============
# Food Code
# ============
@login_required(login_url='login')
def foods(request):
    foods_list = Food.objects.all()
    context = {'foods': foods_list}
    return render(request, 'food/food/foods.html', context)


@login_required(login_url='login')
def edit_food(request, pk):
    food = Food.objects.get(id=pk)
    form = FoodForm(instance=food)
    if request.method == "POST":
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            food = form.save(commit=False)
            food.price_per_serving = round(food.price / food.servings_per_container, 2)
            food.price_per_100cal = round((food.price_per_serving / food.calories) * 100, 2)
            form.save()
            return redirect('foods')

    context = {'form': form, 'food': food}
    return render(request, 'food/food/edit_food.html', context)


@login_required(login_url='login')
def delete_food(request, pk):
    food = Food.objects.get(id=pk)
    context = {'food': food}
    if request.method == "POST":
        food.delete()
        return redirect('foods')
    return render(request, 'food/food/confirm_delete.html', context)


@login_required(login_url='login')
def create_food(request):
    form = FoodForm()
    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.price_per_serving = food.price / food.servings_per_container
            food.price_per_100cal = round((food.price_per_serving / food.calories) * 100, 2)
            form.save()
            return redirect('foods')

    context = {'form': form}
    return render(request, 'food/food/create_food.html', context)


# ============
# Recipes Code
# ============
@login_required(login_url='login')
def recipes(request):
    recipes_list = Recipe.objects.all()
    context = {'recipes': recipes_list}
    return render(request, 'food/recipe/recipes.html', context)


@login_required(login_url='login')
def delete_recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    context = {'recipe': recipe}
    if request.method == "POST":
        recipe.delete()
        return redirect('recipes')
    return render(request, 'food/recipe/delete_recipe.html', context)


@login_required(login_url='login')
def create_recipe(request):
    form = RecipeForm()
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
        return redirect('create_recipe_step2', recipe.pk)

    context = {'form': form, }
    return render(request, 'food/recipe/create_recipe.html', context)


@login_required(login_url='login')
def recipe_details(request, pk):
    recipe = Recipe.objects.get(id=pk)
    ingredients = Ingredient.objects.all().filter(recipe=recipe)
    context = {'recipe': recipe, 'ingredients': ingredients}
    return render(request, 'food/recipe/recipe_details.html', context)


@login_required(login_url='login')
def create_recipe_step2(request, pk):
    recipe = Recipe.objects.get(id=pk)
    ingredients = Ingredient.objects.all().filter(recipe=recipe)
    total_price = 0
    total_calories = 0
    total_carb = 0
    total_fat = 0
    total_protein = 0
    for i in ingredients:
        total_price += i.price * i.serving_amount
        total_calories += i.calories * i.serving_amount
        total_carb += i.carb * i.serving_amount
        total_fat += i.fat * i.serving_amount
        total_protein += i.protein * i.serving_amount

    recipe.price_per_serving = round(total_price / recipe.servings, 1)
    recipe.calories = round(total_calories / recipe.servings, 1)
    recipe.carb = round(total_carb / recipe.servings, 1)
    recipe.fat = round(total_fat / recipe.servings, 1)
    recipe.protein = round(total_protein / recipe.servings, 1)
    if recipe.calories != 0:
        recipe.price_per_100cal = round((recipe.price_per_serving / recipe.calories) * 100, 1)
    recipe.save()

    context = {'recipe': recipe, 'ingredients': ingredients}
    return render(request, 'food/recipe/create_recipe_step2.html', context)


@login_required(login_url='login')
def add_ingredient(request, pk, food):
    form = IngredientForm()
    recipe = Recipe.objects.get(id=pk)
    food = Food.objects.get(id=food)
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.name = food.name
            ingredient.price = food.price
            ingredient.calories = food.calories
            ingredient.fat = food.fat
            ingredient.serving_amount = food.serving_size
            ingredient.carb = food.carb
            ingredient.protein = food.protein
            ingredient.unit = food.unit
            form.save()
        return redirect('create_recipe_step2', recipe.pk)
    context = {'recipe': recipe, 'food': food, 'form': form}
    return render(request, 'food/recipe/add_ingredient.html', context)


@login_required(login_url='login')
def search_ingredient(request, pk):
    recipe = Recipe.objects.get(id=pk)
    query = request.GET.get('q')
    qs = Food.objects.all()[:10]
    if query is not None:
        lookups = Q(name__icontains=query)
        qs = Food.objects.filter(lookups)
        # qs = Article.objects.search(query)
    context = {
        "object_list": qs,
        'recipe': recipe
    }
    return render(request, "food/recipe/search_ingredient.html", context=context)


@login_required(login_url='login')
def meal_details(request, pk):
    meal = MealPlan.objects.get(id=pk)
    context = {'meal': meal}
    return render(request, "food/meal/meal_details.html", context=context)
