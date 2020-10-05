# app/models.py

import datetime

from app import app, db, bcrypt

import jwt

from sqlalchemy import Column, Integer, DateTime, BigInteger, ForeignKey, Numeric, String, JSON, ARRAY, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=datetime.datetime.now())
    last_updated = Column(DateTime, default=None)


class User(db.Model, BaseModel):
    """ User Model for storing user related details """
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.date_created = datetime.datetime.now()

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = ExpiredToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class ExpiredToken(db.Model, BaseModel):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'expired_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = ExpiredToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class UserKYCModel(db.Model, BaseModel):
    __tablename__ = 'user_kyc'

    full_names = Column(String(35), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), index=True)
    email = Column(String(35), nullable=False)

    def __init__(self, full_names, user_id, email):
        self.full_names = full_names
        self.user_id = user_id
        self.email = email


class Item(db.Model, BaseModel):
    __tablename__ = 'items'

    item = Column(String(35), nullable=False)
    item_name = Column(String(35), nullable=False)
    item_description = Column(String(35), nullable=False)

    def __init__(self, item, item_name, item_description):
        self.item = item
        self.item_name = item_name
        self.item_description = item_description


class UserItem(db.Model, BaseModel):
    __tablename__ = 'user_item'

    user_id = Column(BigInteger, ForeignKey('users.id'), index=True)
    item_id = Column(BigInteger, ForeignKey('items.id'), index=True)

    def __init__(self, user_id, item_id):
        self.user_id = user_id
        self.item_id = item_id
