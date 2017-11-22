from elasticsearch import NotFoundError
import graphene
from graphene import relay
from graphene.types.json import JSONString

from .documents import UserDoc, ReportDoc
from .paginator import Paginator
from . import search


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
        return cls(
            id=user.meta.id,
            name=user.name,
            openid_uid=user.openid_uid,
            email=user.email,
            extra=user.extra._d_,
        )

    @classmethod
    def get_node(cls, info, id):
        try:
            user = UserDoc.get(id, using=info.context['es'])
        except NotFoundError:
            return None
        return cls.from_es(user)

    def resolve_reports(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        response = search.reports_by_author(info.context['es'], self.id, paginator)
        total = response.hits.total
        page_info = paginator.get_page_info(total)

        edges = []
        for i, report in enumerate(response):
            cursor = paginator.get_edge_cursor(i + 1)
            node = Report.from_es(report, author=self)
            edges.append(ReportConnection.Edge(node=node, cursor=cursor))

        return ReportConnection(page_info=page_info, edges=edges, total_count=total)
