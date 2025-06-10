from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Cars(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(String, nullable=False)
    is_taken = Column(Boolean, default=False)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    image = Column(String, nullable=False, default='default.png')

    place = relationship('Place', backref='cars')
