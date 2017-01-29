import datetime

from flask import url_for, current_app, g
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired
)
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.errors import ValidationError, ConflictError, UnauthorizedError


class User(db.Model):
    """
    The User creates and manages bucketlists.
    At the database level, users are stored within a table : `users`
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    bucketlists = db.relationship('Bucketlist', backref='created_by',
                                  lazy='dynamic', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def to_json(self):
        return {
            'username': self.username,
            'id': self.id
        }

    def from_json(self, json):
        """
        Creates a User object using parameters from the json data

        :param json: Parameters, in JSON Format, to create User object
        :return: an instance of User object
        """
        if not json:
            raise ValidationError('invalid request: no body provided in '
                                  'request')
        try:
            self.username = json['username']
            self.password = json['password']

            if not json['username']:
                raise ValidationError("username cannot be empty")
            if not json['password']:
                raise ValidationError("password cannot be empty")

            if User.query.filter_by(
                    username=self.username).first() is not None:
                raise ConflictError("user already exists")
        except KeyError as e:
            raise ValidationError(
                "you must provide both username and password")
        return self

    def from_login_json(self, json):
        if not json:
            raise UnauthorizedError('no body provided in '
                                    'request')
        try:
            username = json['username']
            password = json['password']
        except KeyError:
            raise UnauthorizedError(
                "you must provide both username and password")
        if not json['username']:
            raise UnauthorizedError("username cannot be empty")
        if not json['password']:
            raise UnauthorizedError("password cannot be empty")
        user = User.query.filter_by(username=username).first()
        if not user:
            raise UnauthorizedError(
                "authentication error: User does not exist")
        if not user.verify_password(password):
            raise UnauthorizedError("wrong password provided")
        return user

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        Verifies the authentication token that the User provides

        :param token: token string
        :return: authenticated User instance if successful
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            credentials = s.loads(token)
        except SignatureExpired:
            raise UnauthorizedError("authentication error: token has expired")
        except BadSignature:
            raise UnauthorizedError("authentication error: token is invalid")
        user = User.query.get(credentials['id'])
        return user

    def __repr__(self):
        return "User: {}".format(self.username)


class Bucketlist(db.Model):
    """
    A Bucketlist represents a collection of Items managed by the User.
    Each Bucketlist must be owned by a User; and can have multiple Items within
    it.
    At the database level, Bucketlists are stored in the table `bucketlists`.
    """
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.String(1000), default="")
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='bucketlist', lazy='dynamic',
                            cascade='all, delete-orphan')

    def validate_json_keys(self, json):
        if len(json.keys()) > 2:
            return False
        if len(json.keys()) == 2:
            return 'name' in json.keys() and 'description' in json.keys()
        else:
            return 'name' in json.keys() or 'description' in json.keys()

    def from_json(self, json):
        if not json:
            raise ValidationError("invalid request: no data provided")
        if not self.validate_json_keys(json):
            raise ValidationError(
                'only name and/or description can be in body')
        try:
            self.name = json['name']

            if not self.name:
                raise ValidationError('bucketlist name cannot be empty')

            if 'description' in json and json['description']:
                self.description = json['description']
        except KeyError:
            raise ValidationError('name must both be provided')
        self.user_id = g.user.id
        return self

    def update_from_json(self, json):
        if not json:
            raise ValidationError('request cannot be empty')
        elif not self.validate_json_keys(json):
            raise ValidationError(
                'only name and/or description can be updated')
        elif 'name' in json:
            if json['name']:
                self.name = json['name']
            else:
                raise ValidationError('bucketlist name cannot be empty')
        elif 'description' in json:
            self.description = json['description']
        else:
            raise ValidationError('invalid body in request')
        self.date_modified = datetime.datetime.now()
        return self

    def get_url(self):
        return url_for('api.get_bucketlist', bucketlist_id=self.id,
                       _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'created_by': self.user_id,
            'items': [item.get_url() for item in self.items]
        }

    def __repr__(self):
        return "Bucketlist: {}".format(self.name)


class Item(db.Model):
    """
    An Item represents an entry on the Bucketlist.
    At the database level, Items are stored in the table `items`
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False, index=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(100))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def validate_json_keys(self, json):
        """
        Helper method to check that the request body JSON has valid keys

        :return: True if JSON had valid keys; else False
        """
        if len(json.keys()) > 3:
            return False
        if len(json.keys()) == 3:
            return 'name' in json.keys() and 'done' in json.keys() and \
                   'priority' in json.keys()
        else:
            return all([key in ('name', 'done', 'priority') for key in json.keys()])

    def get_url(self):
        """
        Returns the full URL of this Item object.
        """
        return url_for('api.get_item', item_id=self.id, _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'done': self.done,
            'bucketlist_id': self.bucketlist_id,
            'priority': self.priority
        }

    def update_from_json(self, json):
        """
        Updates an existing Item with properties defined in the JSON file
        passed

        :return: instance of Item
        """
        if not json:
            raise ValidationError("invalid request: no JSON data has been"
                                  "provided.")
        if not self.validate_json_keys(json):
            raise ValidationError("only name and/or done and/or priority can "
                                  "be in request body")
        if 'name' in json:
            if json['name']:
                self.name = json['name']
            else:
                raise ValidationError('invalid request: name cannot be empty')
        if 'done' in json:
            if json['done'] and json['done'] in ('true', 'false'):
                if json['done'] == 'true':
                    self.name = True
                else:
                    self.name = False
            else:
                raise ValidationError(
                    'invalid request: done can only be true or false')
        if 'priority' in json:
            if json['priority']:
                self.name = json['priority']
            else:
                raise ValidationError(
                    'invalid request: priority cannot be empty')
        self.date_modified = datetime.datetime.now()
        return self

    def from_json(self, json):
        """
        Constructs an Item object with properties in the JSON object passed.

        :param json: JSON object with Item properties
        :return: an Item instance
        """
        if not json:
            raise ValidationError("invalid request: no JSON data has been "
                                  "provided to construct Item")
        try:
            self.name = json['name']
            if not self.name:
                raise ValidationError('invalid request: Item name cannot be '
                                      'empty.')

            if 'done' in json:
                if json['done']:
                    self.done = json['done']
                else:
                    raise ValidationError("invalid request: done cannot be "
                                          "empty")
            if 'priority' in json:
                if json['priority']:
                    self.priority = json['priority']
                else:
                    raise ValidationError(
                        "invalid request: priority cannot be "
                        "empty")
        except KeyError:
            raise ValidationError(
                "invalid request: Item name must be provided")
        self.date_created = datetime.datetime.now()
        return self

    def __repr__(self):
        return "Item: {}".format(self.name)
