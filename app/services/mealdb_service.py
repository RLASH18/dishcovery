import requests
from flask import current_app

class MealDbService:

    @staticmethod
    def _get_base_url():
        return current_app.config.get('MEALDB_BASE_URL')

    @staticmethod
    def search_by_ingredient(ingredient):
        """Search meals that contain a specific ingredient"""
        url = f"{MealDbService._get_base_url()}/filter.php?i={ingredient}"
        
        response = requests.get(url)
        data = response.json()

        return data.get('meals') or []
    
    @staticmethod
    def get_recipe_details(meal_id):
        """Fetch full recipe details including instructions and image"""
        url = f"{MealDbService._get_base_url()}/lookup.php?i={meal_id}"

        response = requests.get(url)
        data = response.json()
        meals = data.get('meals')

        return meals[0] if meals else None
    
    @staticmethod
    def search_by_name(name):
        """Search for a specific meal by name"""
        url = f"{MealDbService._get_base_url()}/search.php?s={name}"

        response = requests.get(url)
        data = response.json()

        return data.get('meals') or []


