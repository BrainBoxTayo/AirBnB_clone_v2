#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import os
from models.base_model import BaseModel, Base
from sqlalchemy.sql import text

HBNB_MYSQL_DB = os.getenv("HBNB_MYSQL_DB")
HBNB_MYSQL_USER = os.getenv("HBNB_MYSQL_USER")
HBNB_MYSQL_PWD = os.getenv("HBNB_MYSQL_PWD")
HBNB_MYSQL_HOST = os.getenv("HBNB_MYSQL_HOST")
HBNB_ENV = os.getenv("HBNB_ENV")
dialect = 'mysql'
driver = 'mysqldb'


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        super().__init__()
        self.__engine = create_engine(
            f"{dialect}+{driver}://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}", pool_pre_ping=True)

        if (HBNB_ENV == 'test'):
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        get all obects of type {class}
        """

        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        objects = []
        if self.__session is None:
             self.reload()
        if cls is None:
            for cls_name, cls_obj in classes.items():
                objects.extend(self.__session.query(cls_obj).all())
        else:
            # Handle both str and class input
            cls_name = cls if isinstance(cls, str) else cls.__name__
            if cls_name in classes:
                objects = self.__session.query(classes[cls_name]).all()
        new_dict = {}

        for user in objects:
            new_dict[f"{user.__class__.__name__}.{user.id}"] = user

        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj if not none"""
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """create all tables in the database"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
