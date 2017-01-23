import datetime

from flask import url_for, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired
)

from app import db
from app.errors import ValidationError, ConflictError


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
            'username': self.username
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

            if User.query.filter_by(username=self.username).first() is not None:
                raise ConflictError("user already exists")
        except KeyError as e:
            raise ValidationError(
                "you must provide both username and password")
        return self

    def from_login_json(self, json):
        if not json:
            raise ValidationError('no body provided in '
                                  'request')
            # return bad_request('no body provided in request')
        try:
            username = json['username']
            password = json['password']
        except KeyError:
            raise ValidationError(
                "you must provide both username and password")
        if not json['username']:
            raise ValidationError("username cannot be empty")
        if not json['password']:
            raise ValidationError("password cannot be empty")
        user = User.query.filter_by(username=json['username']).first()
        if not user:
            raise ValidationError("authentication error: User does not exist")
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
            raise ValidationError("authentication error: token has expired")
        except BadSignature:
            raise ValidationError("authentication error: token is invalid")
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

    def from_json(self, json):
        if not json:
            raise ValidationError("invalid request: no data provided")
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
            raise ValidationError('invalid request')
        elif 'name' in json and json['name']:
            self.name = json['name']
        elif 'description' in json and json['description']:
            self.description = json['description']
        else:
            raise ValidationError('invalid request')
        self.date_modified = datetime.datetime.now()
        return self

    def get_url(self):
        return url_for('api.get_bucketlist', bucketlist_id=self.id,
                       _external=True)

    def to_json(self):
        return {
            'name': self.name
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
        if 'name' in json:
            if json['name']:
                self.name = json['name']
            else:
                raise ValidationError('invalid request: name cannot be empty')
        if 'done' in json:
            if json['done']:
                self.name = json['done']
            else:
                raise ValidationError('invalid request: done cannot be empty')
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
                    raise ValidationError("invalid request: priority cannot be "
                                          "empty")
        except KeyError:
            raise ValidationError(
                "invalid request: Item name must be provided")
        self.date_created = datetime.datetime.now()
        return self

    def __repr__(self):
        return "Item: {}".format(self.name)
