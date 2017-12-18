import graphene
from graphene import relay

from .types import Report, User, LoginShortcut
from .documents import UserDoc
from .paginator import Paginator
from .sanitizers import extract_text
from .utils import get_viewer
from . import search


class SearchReportsConnection(relay.Connection):
    total_count = graphene.Int()

    class Meta:
        node = Report


def get_authors(ids, *, es, index):
    response = UserDoc.mget(ids, using=es, index=index)
    return {a.meta.id: User.from_es(a) for a in response}


class Query:
    highlight_help = ('Whether search matches should be marked with tag <mark>.'
        ' Default: false')

    node = relay.Node.Field()
    search_reports = relay.ConnectionField(
        SearchReportsConnection,
        description='Fulltext search in Reports.',
        query=graphene.String(description='Text to search for.'),
        highlight=graphene.Boolean(default_value=False, description=highlight_help),
    )
    viewer = graphene.Field(User, description='Active user viewing API.')
    login_shortcuts = graphene.List(
        LoginShortcut,
        description='Shortcuts for login. Use with LoginByShortcut mutation.',
    )

    def resolve_search_reports(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        query = kwargs.get('query', '')
        query = extract_text(query)
        params = {
            'es': info.context['es'],
            'index': info.context['index'],
            'highlight': kwargs.get('highlight'),
        }
        response = search.query_reports(query, paginator, **params)
        total = response.hits.total
        page_info = paginator.get_page_info(total)

        edges = []
        if len(response) > 0:
            authors = get_authors(ids=[r.author_id for r in response], **info.context)
            for i, report in enumerate(response):
                cursor = paginator.get_edge_cursor(i + 1)
                node = Report.from_es(report, author=authors[report.author_id])
                edges.append(SearchReportsConnection.Edge(node=node, cursor=cursor))

        return SearchReportsConnection(page_info=page_info, edges=edges, total_count=total)

    def resolve_viewer(self, info, **kwargs):
        return get_viewer(info)

    def resolve_login_shortcuts(self, info, **kwargs):
        response = search.login_shortcuts(**info.context)
        return [LoginShortcut.from_es(ls) for ls in response]
