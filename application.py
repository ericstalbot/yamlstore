from yamlstore import create_app, db
from yamlstore.models import User, YamlDocument
import datetime
import os



application = create_app(
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI'],
    SECRET_KEY = os.environ['SECRET_KEY'],
    )

    
db.create_all() #remove this once we are using a real database  
    
