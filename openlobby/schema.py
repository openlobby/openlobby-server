import re
from elasticsearch import NotFoundError
import graphene
from graphene import relay
from graphene.types.json import JSONString

from .documents import AuthorDoc, ReportDoc


class Author(graphene.ObjectType):
    name = graphene.String()
    extra = JSONString()

    class Meta:
        interfaces = (relay.Node, )

    @classmethod
    def get_node(cls, info, id):
        try:
            author = AuthorDoc.get(id, using=info.context['es'])
        except NotFoundError:
            return None

        return cls(id=author.meta.id, name=author.name, extra=author.extra._d_)


class Report(graphene.ObjectType):
    author = graphene.Field(Author)
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
    def get_node(cls, info, id):
        try:
            report = ReportDoc.get(id, using=info.context['es'])
        except NotFoundError:
            return None

        author = Author.get_node(info, report.author_id)
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
