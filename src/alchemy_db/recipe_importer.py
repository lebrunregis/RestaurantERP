import json
import os
from urllib.parse import unquote
import pandas as pd
import ast
import re
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
        with SessionLocal() as session:
                models.base_model.Base.metadata.drop_all(engine)
                session.commit()
                models.base_model.Base.metadata.create_all(engine)
                session.commit()

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