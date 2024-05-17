import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin



class Event(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Event'

    id_event = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key = True, autoincrement = True)
    type_event = sqlalchemy.Column(sqlalchemy.Integer)
    day_event = sqlalchemy.Column(sqlalchemy.Date)
    time_event = sqlalchemy.Column(sqlalchemy.Time, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String)
    writer_group = sqlalchemy.Column(sqlalchemy.INTEGER)
    

