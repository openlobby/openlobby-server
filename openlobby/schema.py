import graphene

from openlobby.core.mutations import Mutation as CoreMutation
from openlobby.core.schema import Query as CoreQuery
from openlobby.core.types import User, Report, LoginShortcut


class Query(CoreQuery, graphene.ObjectType):
    pass


class Mutation(CoreMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation,
    types=[User, Report, LoginShortcut])
