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
        df = pd.read_csv('recipes_w_search_terms.csv')

        # Import DataFrame into PostgreSQL
        df.to_sql('recipes', engine, if_exists='replace', index=False)