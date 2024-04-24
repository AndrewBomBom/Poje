import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(SqlAlchemyBase, UserMixin):
      __tablename__ = 'Users'

      id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True)
      name = sqlalchemy.Column(sqlalchemy.String)
      lastname = sqlalchemy.Column(sqlalchemy.String)
      group_num = sqlalchemy.Column(sqlalchemy.Integer)
      podgroup_num = sqlalchemy.Column(sqlalchemy.Integer)
      Starosta = sqlalchemy.Column(sqlalchemy.Boolean)
      hashed_password = sqlalchemy.Column(sqlalchemy.String)
