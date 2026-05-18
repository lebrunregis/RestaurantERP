import os

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
        recipes = pd.read_csv('recipes_w_search_terms.csv')

        # If ingredients are stored as strings like "['salt', 'pepper']"
        recipes['ingredients'] = recipes['ingredients'].apply(ast.literal_eval)

        # Flatten all ingredient lists into one list
        all_ingredients = [
        ingredient
        for sublist in recipes['ingredients']
                for ingredient in sublist
        ]
        # Remove duplicates
        unique_ingredients = pd.DataFrame({
                'ingredient': pd.unique(all_ingredients)
        })
        recipe_ingredients = 
        # Import DataFrames into PostgreSQL
        unique_ingredients.to_sql('ingredients', engine, if_exists='replace', index=False)  
        recipes.to_sql('recipes', engine, if_exists='replace', index=False)