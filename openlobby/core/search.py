from .documents import ReportDoc
from .models import ReportSort


HIGHLIGHT_PARAMS = {
    "number_of_fragments": 0,
    "pre_tags": ["<mark>"],
    "post_tags": ["</mark>"],
}


def search_reports(
    paginator,
    *,
    query=None,
    highlight=False,
    author_id=None,
    sort=ReportSort.PUBLISHED,
    reversed=False,
):
    fields = [
        "title",
        "body",
        "received_benefit",
        "provided_benefit",
        "our_participants",
        "other_participants",
    ]
    s = ReportDoc.search()

    s = s.exclude("term", is_draft=True)
    s = s.exclude("exists", field="superseded_by_id")

    if author_id:
        s = s.filter("term", author_id=author_id)

    if query:
        s = s.query("multi_match", query=query, fields=fields)

    if highlight:
        s = s.highlight(*fields, **HIGHLIGHT_PARAMS)

    if sort == ReportSort.PUBLISHED:
        s = s.sort("published" if reversed else "-published")
    elif sort == ReportSort.DATE:
        s = s.sort("date" if reversed else "-date")
    elif sort == ReportSort.RELEVANCE:
        s = s.sort({"_score": {"order": "asc" if reversed else "desc"}}, "-published")

    s = s[paginator.slice_from : paginator.slice_to]
    return s.execute()
