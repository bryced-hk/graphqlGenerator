from sqlalchemy import Column, DateTime, Integer, String

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from connections.database import Base, db_session
from models.products.model import Products as ProductsModel, Products_gql


# Defines graphql create Mutation
class createProducts(graphene.Mutation):
    class Input:
        id = graphene.Int()
        isbn = graphene.Int()
        title = graphene.String()
        date_created = graphene.DateTime()
        
    ok = graphene.Boolean()
    products = graphene.Field(Products_gql)

    @classmethod
    def mutate(cls, _, args, context, info):
        products = ProductsModel(id=args.get('id'),
                         isbn=args.get('isbn'),
                         title=args.get('title'),
                         date_created=args.get('date_created'),
                         
                         )      
        db_session.add(products)
        db_session.commit()
        ok = True
        return createProducts(products=products, ok=ok)


def resolve_find_products(self, args, context, info):
        query = Products_gql.get_query(context)
        id = args.get('id')
        return query.filter(ProductsModel.id == id).first()


# Defines graphql queries
class ProductsQueries():
    products = SQLAlchemyConnectionField(Products_gql)
    find_products = graphene.Field(lambda: Products_gql, name=graphene.String())
    all_products = SQLAlchemyConnectionField(Products_gql)

    def resolve_find_products(self, args, context, info):
        return resolve_find_products(self, args, context, info)


# Defines graphql mutations
class ProductsMutations():
    create_products = createProducts.Field()