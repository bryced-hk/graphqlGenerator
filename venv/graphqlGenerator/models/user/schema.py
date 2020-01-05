from sqlalchemy import Column, DateTime, Integer, String

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from connections.database import Base, db_session
from models.user.model import User as UserModel, User_gql


# Defines graphql create Mutation
class createUser(graphene.Mutation):
    class Input:
        id = graphene.Int()
        name = graphene.String()
        location = graphene.String()
        date_created = graphene.DateTime()
        
    ok = graphene.Boolean()
    user = graphene.Field(User_gql)

    @classmethod
    def mutate(cls, _, args, context, info):
        user = UserModel(id=args.get('id'),
                        name=args.get('name'),
                        location=args.get('location'),
                        date_created=args.get('date_created'))

        db_session.add(user)
        db_session.commit()
        ok = True
        return createUser(user=user, ok=ok)


def resolve_find_user(self, args, context, info):
        query = User_gql.get_query(context)
        name = args.get('name')
        return query.filter(UserModel.name == name).first()


# Defines graphql queries
class UserQueries():
    user = SQLAlchemyConnectionField(User_gql)
    find_user = graphene.Field(lambda: User_gql, name=graphene.String())
    all_users = SQLAlchemyConnectionField(User_gql)

    def resolve_find_user(self, args, context, info):
        return resolve_find_user(self, args, context, info)


# Defines graphql queries
class UserMutations():
    create_user = createUser.Field()