import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from connections.database import db_session

from models.permission.schema import PermissionQueries, PermissionMutations
from models.permission.model import Permission_gql
from models.user.schema import UserQueries, UserMutations
from models.user.model import User_gql
from models.products.schema import ProductsQueries, ProductsMutations
from models.products.model import Products_gql


# Sets up graphql Queries
class Query(PermissionQueries,
            UserQueries,
            ProductsQueries,
             graphene.ObjectType):
    node = relay.Node.Field()


# Sets up graphql Mutations
class Mutation(PermissionMutations,
               UserMutations,
               ProductsMutations,
                graphene.ObjectType):
    pass


# Combines queries, mutations, and types to define graphql schema
schema = graphene.Schema(query=Query, mutation=Mutation, types=[Permission_gql,
                                                                User_gql,
                                                                Products_gql,
                                                                ])