import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(SqlAlchemyBase, UserMixin):
      __tablename__ = 'User'

      id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True)
      email = sqlalchemy.Column(sqlalchemy.String, unique = True, index = True,nullable=True)
      name = sqlalchemy.Column(sqlalchemy.String)
      lastname = sqlalchemy.Column(sqlalchemy.String)
      group_num = sqlalchemy.Column(sqlalchemy.Integer)
      podgroup_num = sqlalchemy.Column(sqlalchemy.Integer, nullable = True)
      Starosta = sqlalchemy.Column(sqlalchemy.Boolean, nullable = True)
      hashed_password = sqlalchemy.Column(sqlalchemy.String)

      def set_password(self, password):
            self.hashed_password = generate_password_hash(password)

      def check_password(self, password):
            return check_password_hash(self.hashed_password, password)
