from .documents import ReportDoc

HIGHLIGHT_PARAMS = {
    'number_of_fragments': 0,
    'pre_tags': ['<mark>'],
    'post_tags': ['</mark>'],
}


def query_reports(query, paginator, *, highlight=False, sort='date', reversed=False):
    fields = ['title', 'body', 'received_benefit', 'provided_benefit',
              'our_participants', 'other_participants']
    s = ReportDoc.search()
    s = s.exclude('term', is_draft=True)
    if query != '':
        s = s.query('multi_match', query=query, fields=fields)
    if highlight:
        s = s.highlight(*fields, **HIGHLIGHT_PARAMS)
    # the following exercise is because `-_score` simply does not work, so the following workaround is used
    sort_dict = dict()
    sort_dict[sort] = dict(order='asc' if reversed else 'desc')

    s = s.sort(sort_dict)
    s = s[paginator.slice_from:paginator.slice_to]
    return s.execute()


def reports_by_author(author_id, paginator):
    s = ReportDoc.search()
    s = s.exclude('term', is_draft=True)
    s = s.filter('term', author_id=author_id)
    s = s.sort('-date')
    s = s[paginator.slice_from:paginator.slice_to]
    return s.execute()
