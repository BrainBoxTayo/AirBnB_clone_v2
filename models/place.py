#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table, Integer, Float
from sqlalchemy.orm import relationship
import os
from models import storage
from models.review import Review
from models.amenity import Amenity

# Association Table for many-to-many relationship
place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id",  ForeignKey(
                          "places.id"), nullable=False, primary_key=True),
                      Column("amenity_id", ForeignKey("amenities.id"),
                             nullable=False, primary_key=True),

                      )


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(128), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True, default=0.0)
    longitude = Column(Float, nullable=True, default=0.0)
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        amenities = relationship(
            "Amenity", secondary="place_amenity", viewonly=False, back_populates='place_amenities')
        reviews = relationship(
            "Review", cascade="all, delete-orphan", backref="places")
    else:
        @property
        def reviews(self):
            # returns all instances of reviews with place_id == Place.id
            all_reviews = storage.all(Review)
            review_list = [value for value in all_reviews.values() if (
                value.place_id == self.id)]
            return review_list

        @property
        def amenities(self):
            # returns the list of Amenity instances based on the attribute
            # amenity_ids
            if (len(self.amenity_ids) > 0):
                all_amenities = storage.all(Amenity)
                amenity_list = [value for value in all_amenities.values() if (
                    value.id in self.amenity_ids)]
                return amenity_list
            else:
                return []

        @amenities.setter
        def amenities(self, obj):
            if isinstance(obj, Amenity):
                # append the obj to amenity_ids
                self.amenity_ids.append(obj.id)
            else:
                pass
