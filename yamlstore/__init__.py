from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import SQLAlchemyAdapter, UserManager

app = Flask(__name__)
db = SQLAlchemy(app)

def create_app(**config):

    
    app.config.from_object('yamlstore.default_config')
    app.config.update(**config)
    
    from yamlstore.models import User
    
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)   

    import yamlstore.views
    
    return app













