import graphene

from openlobby.core.api.mutations import Mutation as CoreMutation
from openlobby.core.api.schema import Query as CoreQuery
from openlobby.core.api.types import User, Report, LoginShortcut


class Query(CoreQuery, graphene.ObjectType):
    pass


class Mutation(CoreMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation,
    types=[User, Report, LoginShortcut])
