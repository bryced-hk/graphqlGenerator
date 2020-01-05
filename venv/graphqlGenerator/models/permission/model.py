from sqlalchemy import Column, DateTime, Integer, String

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from connections.database import Base, db_session

# Defines base class for SQLAlchemy
class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer(), primary_key=True)
    userId = Column(Integer())
    productId = Column(Integer())
    

# Defines specific table metaData
class Permission_gql(SQLAlchemyObjectType):
    class Meta:
        model = Permission
        interfaces = (relay.Node, )