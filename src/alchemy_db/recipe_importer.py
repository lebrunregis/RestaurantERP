import json
import os
from urllib.parse import unquote
import pandas as pd
import ast
import re

from sqlalchemy import func, select

from .models.recipes_model import Recipe

from .models.ingredients_model import Ingredient
from .models.recipe_ingredients_model import RecipeIngredient
from . import models

from .session import session

from .session.session import SessionLocal
from .database.database import engine


def extract_serving_size(s):
    match = re.search(r"\((-?\d+)\s*g\)", s)
    val = None
    if match:
        val = int(match.group(1))
    else:
           print(f"The serving size doesn't match the format. {s}")
    return val

def import_recipes():
        # Load Excel file
        recipes :pd.DataFrame = pd.read_csv('recipes_w_search_terms.csv')
        # Filter result based on database criterias

        recipes.drop(recipes[recipes['description'].str.len()< 25].index, inplace=True)
        recipes.drop(recipes[recipes['description'].str.len() > 500].index, inplace=True)
        recipes.drop(recipes[recipes['description'].str.strip().eq('')].index, inplace=True)
        recipes.drop(recipes[recipes['description'].isnull()].index, inplace=True)
        recipes.drop(recipes[recipes['steps'].str.len() > 500].index, inplace=True)
        recipes.drop(recipes[recipes['steps'].str.len() < 25].index, inplace=True)
        recipes.drop(recipes[recipes['steps'].str.strip().eq('')].index, inplace=True)
        recipes.drop(recipes[recipes['steps'].isnull()].index, inplace=True)
        recipes.drop(recipes[recipes['ingredients_raw_str'].str.len() > 500].index, inplace=True)
        # values conversion
        recipes['ingredients'] = recipes['ingredients'].apply(ast.literal_eval)
        recipes['servings'] = recipes['servings'].astype(int)
        recipes['serving_size'] = recipes['serving_size'].apply(extract_serving_size)
        #extra filtering based on converted data
        recipes.drop(recipes[recipes['serving_size']< 1].index, inplace=True)
        recipes.drop(recipes[recipes['serving_size']> 1000].index, inplace=True)
        recipes.drop(recipes[recipes['servings']< 1].index, inplace=True)
        recipes.drop(recipes[recipes['servings']> 1000].index, inplace=True)
        # Drop recipes with the same name
        recipes = recipes.drop_duplicates(subset='name', keep='first')
        # Flatten all ingredient lists into one list
        all_ingredients = [
        ingredient
        for sublist in recipes['ingredients']
                for ingredient in sublist
        ]
        # Remove duplicates
        unique_ingredients = pd.DataFrame({
                'name': pd.unique(pd.Series(all_ingredients))
        })
        unique_ingredients['ingredient_id'] = range(1, len(unique_ingredients) + 1)
        # Fix text formatting errors
        unique_ingredients['name'] = unique_ingredients['name'].apply(unquote)
        # Create lookup dictionary
        ingredient_lookup = dict(zip(unique_ingredients['name'], unique_ingredients['ingredient_id']))

        # Build join table
        recipe_ingredient_list = []

        for _, row in recipes.iterrows():
                recipe_id = row['id']
                for ingredient in row['ingredients']:
                        recipe_ingredient_list.append({
                        'recipe_id': recipe_id,
                        'ingredient_id': ingredient_lookup[unquote(ingredient)]
                        })
        # Dataframe conversion
        recipe_ingredients = pd.DataFrame(recipe_ingredient_list)
        # Remove unnecessary data
        recipes.drop(columns=['ingredients'], inplace=True)
        recipes.drop(columns=['tags'], inplace=True)
        recipes.drop(columns=['search_terms'], inplace=True)
        recipe_ingredients = recipe_ingredients.drop_duplicates()
        # Rename columns for clarity
        recipes = recipes.rename(columns={
               'id':"recipe_id",
               'serving_size':"serving_size_grams",
                                          })

        # Import DataFrames into PostgreSQL
        with SessionLocal() as session:
                unique_ingredients.to_sql('ingredients', engine, if_exists='append', index=False)  
                recipes.to_sql('recipes', engine, if_exists='append', index=False)
                recipe_ingredients.to_sql('recipe_ingredients', engine, if_exists='append', index=False)
                session.commit()
        if(os.getenv('ALCHEMY_ECHO')):
                print('Database import finished!')

def prune_rare_ingredients():
     with SessionLocal() as session:
        # Step 1: Find ingredient IDs that appear in fewer than 5 recipes
        rare_ingredients = (
        session.query(
                RecipeIngredient.ingredient_id,
                func.count(RecipeIngredient.recipe_id).label("recipe_count")
        )
        .group_by(RecipeIngredient.ingredient_id)
        .having(func.count(RecipeIngredient.recipe_id) < 5)
        .subquery()
        )
        # Step 2: Delete Ingredients that match
        ingredients_to_delete = session.query(Ingredient).filter(Ingredient.ingredient_id.in_(select(rare_ingredients.c.ingredient_id)))
        ingredient_count = ingredients_to_delete.count()  # optional, to see how many will be deleted
        ingredients_to_delete.delete(synchronize_session=False)
        # Step 3: Delete associated recipes
        recipes_links = (
        session.query(
                RecipeIngredient.recipe_id
        ).filter(RecipeIngredient.ingredient_id.in_(select(rare_ingredients.c.ingredient_id))).distinct()
        .subquery()
        )
        recipes_to_delete = session.query(Recipe).filter(Recipe.recipe_id.in_(select(recipes_links.c.recipe_id)))
        recipe_count = recipes_to_delete.count()  # optional, to see how many will be deleted
        recipes_to_delete.delete(synchronize_session=False)

        session.commit()
        print(f"✅ Deleted {ingredient_count} ingredients used in fewer than 5 recipes and {recipe_count} associated recipes.")