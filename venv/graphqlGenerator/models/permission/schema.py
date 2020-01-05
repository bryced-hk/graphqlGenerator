from sqlalchemy import Column, DateTime, Integer, String

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from connections.database import Base, db_session
from models.permission.model import Permission as PermissionModel, Permission_gql

# Defines graphql create Mutation
class createPermission(graphene.Mutation):
    class Input:
        id = graphene.Int()
        userId = graphene.Int()
        productId = graphene.Int()
        
    ok = graphene.Boolean()
    permission = graphene.Field(Permission_gql)

    @classmethod
    def mutate(cls, _, args, context, info):
        permission = PermissionModel(id=args.get('id'),
                         userId=args.get('userId'),
                         productId=args.get('productId'),
                         
                         )      
        db_session.add(permission)
        db_session.commit()
        ok = True
        return createPermission(permission=permission, ok=ok)


def resolve_find_permission(self, args, context, info):
        query = Permission_gql.get_query(context)
        id = args.get('id')
        return query.filter(PermissionModel.id == id).first()


# Defines graphql queries
class PermissionQueries():
    permission = SQLAlchemyConnectionField(Permission_gql)
    find_permission = graphene.Field(lambda: Permission_gql, name=graphene.String())
    all_permissions = SQLAlchemyConnectionField(Permission_gql)

    def resolve_find_permission(self, args, context, info):
        return resolve_find_permission(self, args, context, info)


# Defines graphql mutations
class PermissionMutations():
    create_permission = createPermission.Field()