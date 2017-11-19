import re
from elasticsearch import NotFoundError
import graphene
from graphene import relay
from graphene.types.json import JSONString

from .documents import UserDoc, ReportDoc
from .paginator import Paginator
from .mutations import Mutations


class Report(graphene.ObjectType):
    author = graphene.Field(lambda: User)
    date = graphene.String()
    published = graphene.String()
    title = graphene.String()
    body = graphene.String()
    received_benefit = graphene.String()
    provided_benefit = graphene.String()
    extra = JSONString()

    class Meta:
        interfaces = (relay.Node, )

    @classmethod
    def from_es(cls, report, author=None):
        return cls(
            id=report.meta.id,
            author=author,
            date=report.date,
            published=report.published,
            title=report.title,
            body=report.body,
            received_benefit=report.received_benefit,
            provided_benefit=report.provided_benefit,
            extra=report.extra._d_,
        )

    @classmethod
    def get_node(cls, info, id):
        try:
            report = ReportDoc.get(id, using=info.context['es'])
        except NotFoundError:
            return None

        author_type = cls._meta.fields['author'].type
        author = author_type.get_node(info, report.author_id)
        return cls.from_es(report, author)


class ReportConnection(relay.Connection):
    total_count = graphene.Int()

    class Meta:
        node = Report


class SearchReportsConnection(relay.Connection):
    total_count = graphene.Int()

    class Meta:
        node = Report


class User(graphene.ObjectType):
    name = graphene.String()
    openid_uid = graphene.String()
    email = graphene.String()
    extra = JSONString()
    reports = relay.ConnectionField(ReportConnection)

    class Meta:
        interfaces = (relay.Node, )

    @classmethod
    def from_es(cls, user):
        return cls(id=user.meta.id, name=user.name, extra=user.extra._d_)

    @classmethod
    def get_node(cls, info, id):
        try:
            user = UserDoc.get(id, using=info.context['es'])
        except NotFoundError:
            return None
        return cls.from_es(user)

    def resolve_reports(self, info, **kwargs):
        paginator = Paginator(**kwargs)

        s = ReportDoc.search(using=info.context['es'])
        s = s.filter('term', author_id=self.id)
        s = s.sort('-published')
        s = s[paginator.slice_from:paginator.slice_to]
        response = s.execute()

        total = response.hits.total
        page_info = paginator.get_page_info(total)

        edges = []
        for i, report in enumerate(response):
            cursor = paginator.get_edge_cursor(i + 1)
            node = Report.from_es(report, author=self)
            edges.append(ReportConnection.Edge(node=node, cursor=cursor))

        return ReportConnection(page_info=page_info, edges=edges, total_count=total)


def get_authors(es, ids):
    response = UserDoc.mget(ids, using=es)
    return {a.meta.id: User.from_es(a) for a in response}


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    search_reports = relay.ConnectionField(SearchReportsConnection, query=graphene.String())

    def resolve_search_reports(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        query = kwargs.get('query', '')
        query = ' '.join(re.findall(r'(\b\w+)', query))

        s = ReportDoc.search(using=info.context['es'])
        if query != '':
            s = s.query('multi_match', query=query, fields=['title', 'body', 'received_benefit', 'provided_benefit'])
        s = s.sort('-published')
        s = s[paginator.slice_from:paginator.slice_to]
        response = s.execute()

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


schema = graphene.Schema(query=Query, mutation=Mutations, types=[User, Report])
