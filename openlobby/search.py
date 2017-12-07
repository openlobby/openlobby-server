from .documents import ReportDoc, OpenIdClientDoc


HIGHLIGHT_PARAMS = {
    'number_of_fragments': 0,
    'pre_tags': ['<mark>'],
    'post_tags': ['</mark>'],
}


def query_reports(query, paginator, *, es, index, highlight=False):
    fields = ['title', 'body', 'received_benefit', 'provided_benefit',
        'our_participants', 'other_participants']
    s = ReportDoc.search(using=es, index=index)
    if query != '':
        s = s.query('multi_match', query=query, fields=fields)
    if highlight:
        s = s.highlight(*fields, **HIGHLIGHT_PARAMS)
    s = s.sort('-published')
    s = s[paginator.slice_from:paginator.slice_to]
    return s.execute()


def reports_by_author(author_id, paginator, *, es, index):
    s = ReportDoc.search(using=es, index=index)
    s = s.filter('term', author_id=author_id)
    s = s.sort('-published')
    s = s[paginator.slice_from:paginator.slice_to]
    return s.execute()


def login_shortcuts(*, es, index):
    s = OpenIdClientDoc.search(using=es, index=index)
    s = s.filter('term', is_shortcut=True)
    return s.execute()
