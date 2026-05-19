import os
from urllib.parse import unquote
import pandas as pd
import ast
from .models.base_model import Base
from .database import database
from .session import session
from .models import user_model
from .accessors import user_repository

from .session.session import SessionLocal
from .database.database import engine

if(os.getenv('FIRST_TIME_INITIALIZE')):
        with SessionLocal() as session:
                Base.metadata.create_all(engine)
                session.commit()

        # Load Excel file
        recipes :pd.DataFrame = pd.read_csv('recipes_w_search_terms.csv')
        # transform the string into an array of strings safely without using eval
        recipes['ingredients'] = recipes['ingredients'].apply(ast.literal_eval)

        # Flatten all ingredient lists into one list
        all_ingredients = [
        ingredient
        for sublist in recipes['ingredients']
                for ingredient in sublist
        ]
        # Remove duplicates
        unique_ingredients = pd.DataFrame({
                'name': pd.unique(all_ingredients)
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
        # Rename columns for clarity
        recipes.rename(columns={'id':"recipe_id"})
        # Import DataFrames into PostgreSQL
        unique_ingredients.to_sql('ingredients', engine, if_exists='append', index=False)  
        recipes.to_sql('recipes', engine, if_exists='append', index=False)
        recipe_ingredients.to_sql('recipe_ingredients', engine, if_exists='append', index=False)