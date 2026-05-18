from flask import Flask

app = Flask(__name__)
from src.flask_front.routing import *