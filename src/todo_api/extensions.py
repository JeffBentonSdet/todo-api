"""Flask extension initialization. Centralizes the creation of extension instances for use with the application factory pattern."""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
