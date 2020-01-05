from sqlalchemy import Column, DateTime, Integer, String

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from connections.database import Base, db_session

# Defines specific table metaData
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer(), primary_key=True)
    isbn = Column(Integer())
    title = Column(String())
    date_created = Column(DateTime())
    

# Defines specific table metaData
class Products_gql(SQLAlchemyObjectType):
    class Meta:
        model = Products
        interfaces = (relay.Node, )