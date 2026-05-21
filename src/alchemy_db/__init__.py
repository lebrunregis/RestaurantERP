import json
import os
from .recipe_importer import import_recipes, prune_rare_ingredients
from .demo_data_importer import import_demo_data
import json
import os
from urllib.parse import unquote

from . import models

from .session.session import SessionLocal
from .database.database import engine

RESET_DATABASE: bool = json.loads(os.getenv('RESET_DATABASE', 'false').lower())
IMPORT_RECIPES: bool = json.loads(os.getenv('IMPORT_RECIPES', 'false').lower())
SET_DEMO_DATA: bool = json.loads(os.getenv('SET_DEMO_DATA', 'false').lower())

def ResetDatabase():
        with SessionLocal() as session:
                models.base_model.Base.metadata.drop_all(engine)
                session.commit()
                models.base_model.Base.metadata.create_all(engine)
                session.commit()

if(RESET_DATABASE):
    ResetDatabase()
    if(IMPORT_RECIPES):
        import_recipes()
        prune_rare_ingredients()
        if(SET_DEMO_DATA):
            import_demo_data()
