import re
import graphene
from graphene import relay

from .types import Report, User
from .documents import UserDoc
from .paginator import Paginator
from .mutations import Mutation
from .utils import get_viewer
from . import search


class SearchReportsConnection(relay.Connection):
    total_count = graphene.Int()

    class Meta:
        node = Report


def get_authors(es, ids):
    response = UserDoc.mget(ids, using=es)
    return {a.meta.id: User.from_es(a) for a in response}


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    search_reports = relay.ConnectionField(SearchReportsConnection, query=graphene.String())
    viewer = graphene.Field(User)

    def resolve_search_reports(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        query = kwargs.get('query', '')
        query = ' '.join(re.findall(r'(\b\w+)', query))
        response = search.query_reports(info.context['es'], query, paginator)
        total = response.hits.total
        page_info = paginator.get_page_info(total)

        edges = []
        if len(response) > 0:
            authors = get_authors(info.context['es'], ids=[r.author_id for r in response])
            for i, report in enumerate(response):
                cursor = paginator.get_edge_cursor(i + 1)
                node = Report.from_es(report, author=authors[report.author_id])
                edges.append(SearchReportsConnection.Edge(node=node, cursor=cursor))

        return SearchReportsConnection(page_info=page_info, edges=edges, total_count=total)

    def resolve_viewer(self, info, **kwargs):
        return get_viewer(info)


schema = graphene.Schema(query=Query, mutation=Mutation, types=[User, Report])
