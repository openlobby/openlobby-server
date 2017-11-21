from .documents import ReportDoc


def query_reports(es, query, paginator):
    s = ReportDoc.search(using=es)
    if query != '':
        s = s.query('multi_match', query=query, fields=['title', 'body', 'received_benefit', 'provided_benefit'])
    s = s.sort('-published')
    s = s[paginator.slice_from:paginator.slice_to]
    return s.execute()


def reports_by_author(es, author_id, paginator):
    s = ReportDoc.search(using=es)
    s = s.filter('term', author_id=author_id)
    s = s.sort('-published')
    s = s[paginator.slice_from:paginator.slice_to]
    return s.execute()
