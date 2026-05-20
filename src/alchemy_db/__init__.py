import json
import os
from urllib.parse import unquote
import pandas as pd
import ast
import re

from .recipe_importer import import_recipes
from . import models

from .database import database
from .session import session
from .accessors import user_repository

from .session.session import SessionLocal
from .database.database import engine


IMPORT_RECIPES: bool = json.loads(os.getenv('IMPORT_RECIPES', 'false').lower())
if(IMPORT_RECIPES):
    import_recipes()