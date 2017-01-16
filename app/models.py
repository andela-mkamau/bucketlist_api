import datetime

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.errors import ValidationError


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
        try:
            self.username = json['username']
            self.password = json['password']

            if not json['username']:
                raise ValidationError("username cannot be empty")
            if not json['password']:
                raise ValidationError("password cannot be empty")

            if User.query.filter_by(username=self.username).first() is not None:
                raise ValidationError("username is taken")
        except KeyError as e:
            raise ValidationError("you must provide both username and password")
        return self

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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
            raise ValidationError("invalid request")
        try:
            self.name = json['name']
            self.user_id = json['user_id']

            if not self.name:
                raise ValidationError('bucketlist name cannot be empty')
            if not self.name or not isinstance(self.user_id, int):
                raise ValidationError('user_id is invalid')

            if 'description' in json and json['description']:
                self.description = json['description']
        except KeyError:
            raise ValidationError('name and user_id must both be provided')
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

    def __repr__(self):
        return "Item: {}".format(self.name)
