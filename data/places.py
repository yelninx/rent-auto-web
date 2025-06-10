from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Place(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    address = Column(String, nullable=False)

    owner = relationship('User', backref='places')
