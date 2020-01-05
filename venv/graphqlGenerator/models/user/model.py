from sqlalchemy import Column, DateTime, Integer, String

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from connections.database import Base

# Defines specific table metaData
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    location = Column(String(50))
    date_created = Column(DateTime)

# Defines specific table metaData
class User_gql(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )
