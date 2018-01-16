import graphene
from graphene import relay

from . import types
from ..models import OpenIdClient
from .paginator import Paginator
from .sanitizers import extract_text
from .. import search
from ..models import User


class SearchReportsConnection(relay.Connection):
    total_count = graphene.Int()

    class Meta:
        node = types.Report


def get_authors(ids):
    users = User.objects.filter(id__in=ids)
    return {u.id: types.User.from_db(u) for u in users}


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
    viewer = graphene.Field(types.User, description='Active user viewing API.')
    login_shortcuts = graphene.List(
        types.LoginShortcut,
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
            authors = get_authors(ids=[r.author_id for r in response])
            for i, report in enumerate(response):
                cursor = paginator.get_edge_cursor(i + 1)
                node = types.Report.from_es(report, author=authors[report.author_id])
                edges.append(SearchReportsConnection.Edge(node=node, cursor=cursor))

        return SearchReportsConnection(page_info=page_info, edges=edges, total_count=total)

    def resolve_viewer(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return types.User.from_db(info.context.user)
        else:
            return None

    def resolve_login_shortcuts(self, info, **kwargs):
        clients = OpenIdClient.objects.filter(is_shortcut=True)
        return [types.LoginShortcut.from_db(c) for c in clients]
