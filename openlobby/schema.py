import re
from elasticsearch import NotFoundError
import graphene
from graphene import relay
from graphene.types.json import JSONString

from .documents import AuthorDoc, ReportDoc
from .paginator import Paginator


class Report(graphene.ObjectType):
    author = graphene.Field(lambda: Author)
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


class Author(graphene.ObjectType):
    name = graphene.String()
    extra = JSONString()
    reports = relay.ConnectionField(ReportConnection)

    class Meta:
        interfaces = (relay.Node, )

    @classmethod
    def from_es(cls, author):
        return cls(id=author.meta.id, name=author.name, extra=author.extra._d_)

    @classmethod
    def get_node(cls, info, id):
        try:
            author = AuthorDoc.get(id, using=info.context['es'])
        except NotFoundError:
            return None
        return cls.from_es(author)

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


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    reports = graphene.List(Report, query=graphene.String())

    def resolve_reports(self, info, query=''):
        s = ReportDoc.search(using=info.context['es'])
        if query != '':
            query = ' '.join(re.findall(r'(\b\w+)', query))
            s = s.query('multi_match', query=query, fields=['title', 'body', 'received_benefit', 'provided_benefit'])
        s = s.sort('-published')
        s = s[:20]
        results = s.execute()

        return [Report.get_node(info, report.meta.id) for report in results]


schema = graphene.Schema(query=Query, types=[Author, Report])
