from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('foods/', views.foods, name='foods'),
    path('recipes/', views.recipes, name='recipes'),
    path('create_food/', views.create_food, name='create_food'),
    path('edit_food/<str:pk>', views.edit_food, name='edit_food'),
    path('delete_food/<str:pk>', views.delete_food, name='delete_food'),
    path('delete_recipe/<str:pk>', views.delete_recipe, name='delete_recipe'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('recipe_details/<str:pk>', views.recipe_details, name='recipe_details'),
    path('create_recipe_step2/<str:pk>', views.create_recipe_step2, name='create_recipe_step2'),
    path('search_ingredient/<str:pk>', views.search_ingredient, name='search_ingredient'),
    path('add_ingredient/<str:pk>/<str:food>', views.add_ingredient, name='add_ingredient'),
    path('add_meal/', views.add_meal, name='add_meal'),
    path('delete_meal/<str:pk>', views.delete_meal, name='delete_meal'),
    path('generate_shopping/', views.generate_shopping, name='generate_shopping'),
    path('meal_details/<str:pk>/', views.meal_details, name='meal_details'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile')
]
