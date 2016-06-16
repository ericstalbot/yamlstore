from flask_wtf import Form
from wtforms import StringField, TextAreaField, Field, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length

from flask_user import UserMixin

from yamlstore import db
    
from flask import json
import yaml    
    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    #reset_password_token = db.Column(db.String(100), nullable=False, default='')

    # User Email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    #first_name = db.Column(db.String(50), nullable=False, default='')
    #last_name = db.Column(db.String(50), nullable=False, default='')

    yaml_documents = db.relationship(
        'YamlDocument', backref='user', lazy='dynamic')
    
    def is_active(self):
      return self.is_enabled
        

class YamlDocument(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(99))
    document = db.Column(db.String(9999))
    json = db.Column(db.String(9999))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        
    def __init__(self, user_id):
    
        self.user_id = user_id
        

class YamlDocumentField(TextAreaField):
    def __init__(self, label='', validators=None, **kwargs):
        super(TextAreaField, self).__init__(label, validators, **kwargs)
        self.data=None
        self.json_string=None
    
    def process_formdata(self, valuelist):
        if valuelist:    
            self.data = valuelist[0]
            try:
                data = yaml.safe_load(self.data)
                json_string = json.htmlsafe_dumps(data, indent='  ')
            except yaml.YAMLError as e: #to do: json error here
                self.json_string = None
                raise ValidationError(str(e))
            else:
                self.json_string = json_string
        else:
            self.data = None
            self.json_string = None
            
class EditDocumentForm(Form):
    title = StringField('title', validators=[
        DataRequired(),
        Length(max=99)])
    document = YamlDocumentField('document', validators=[
        Length(max=9999)])