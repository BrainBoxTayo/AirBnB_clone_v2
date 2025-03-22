#!/usr/bin/python3
""" State Module for HBNB project """
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from models import storage
from models.engine import file_storage
from models.city import City 
import os

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if (os.getenv("HBNB_TYPE_STORAGE")) == 'db':
        cities= relationship("City", backref="states")
    else:
        @property
        def cities(self):
            #Return a list of cities equal to the currrent state id
            city_dict = file_storage.FileStorage().all(City)

            city_list = [value for value in city_dict.values() if (value.state_id == self.id)]
            return city_list