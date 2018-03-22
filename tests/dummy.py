import arrow
from openlobby.core.api.schema import REPORT_SORT_DATE_ID

from openlobby.core.models import Report, User

authors = [
    {
        'id': 1,
        'username': 'wolf',
        'first_name': 'Winston',
        'last_name': 'Wolfe',
        'is_author': True,
        'extra': {'movies': 1},
    },
    {
        'id': 2,
        'username': 'sponge',
        'first_name': 'Spongebob',
        'last_name': 'Squarepants',
        'is_author': True,
    },
    {
        'id': 3,
        'username': 'shaun',
        'first_name': 'Shaun',
        'last_name': 'Sheep',
        'is_author': True,
    },
    {
        'id': 4,
        'username': 'phony',
        'first_name': 'Steven',
        'last_name': 'Erikson',
        'is_author': True,
    },
]

reports = [
    {
        'id': 1,
        'date': arrow.get(2018, 1, 1).datetime,
        'published': arrow.get(2018, 1, 2).datetime,
        'title': 'The Fellowship of the Ring',
        'body': 'Long story short: we got the Ring!',
        'received_benefit': 'The Ring',
        'provided_benefit': '',
        'our_participants': 'Frodo, Gandalf',
        'other_participants': 'Saruman',
    },
    {
        'id': 2,
        'date': arrow.get(2018, 1, 3).datetime,
        'published': arrow.get(2018, 1, 4).datetime,
        'title': 'The Two Towers',
        'body': 'Another long story.',
        'received_benefit': 'Mithrill Jacket',
        'provided_benefit': '',
        'our_participants': 'Frodo, Gimli, Legolas',
        'other_participants': 'Saruman, Sauron',
        'extra': {'rings': 1},
    },
    {
        'id': 3,
        'date': arrow.get(2018, 1, 5).datetime,
        'published': arrow.get(2018, 1, 6).datetime,
        'title': 'The Return of the King',
        'body': 'Aragorn is the King. And we have lost the Ring.',
        'received_benefit': '',
        'provided_benefit': 'The Ring',
        'our_participants': 'Aragorn',
        'other_participants': 'Sauron',
    },
    {
        'id': 4,
        'date': arrow.get(2018, 1, 7).datetime,
        'published': arrow.get(2018, 1, 8).datetime,
        'title': 'The Silmarillion',
        'body': 'Not finished yet.',
        'received_benefit': '',
        'provided_benefit': '',
        'our_participants': '',
        'other_participants': '',
        'is_draft': True,
    },
    {
        'id': 5,
        'date': arrow.get(2018, 1, 9).datetime,
        'published': arrow.get(2018, 1, 10).datetime,
        'title': 'The Hobbit',
        'body': 'Work in progress...',
        'received_benefit': '',
        'provided_benefit': '',
        'our_participants': '',
        'other_participants': '',
        'is_draft': True,
    },
    {
        'id': 6,
        'date': arrow.get(2018, 1, 9).datetime,
        'published': arrow.get(2017, 1, 1).datetime,
        'title': 'Gardens of the moon',
        'body': 'Putting Gandalf to shame? Good story...',
        'received_benefit': 'story',
        'provided_benefit': 'story',
        'our_participants': 'Not Gandalf',
        'other_participants': 'Still no Gandalf',
        'is_draft': False,
    },
]


def prepare_reports():
    author1 = User.objects.create(**authors[0])
    author2 = User.objects.create(**authors[1])
    author3 = User.objects.create(**authors[2])

    Report.objects.create(author=author1, **reports[0])
    Report.objects.create(author=author2, **reports[1])
    Report.objects.create(author=author1, **reports[2])
    Report.objects.create(author=author1, **reports[3])
    Report.objects.create(author=author3, **reports[4])


def prepare_author():
    User.objects.create(**authors[0])


def prepare_report(is_draft=False):
    author = User.objects.create(**authors[0])
    Report.objects.create(author=author, is_draft=is_draft, **reports[0])


def search_reports_query(sort):
    template = """
    query {
        searchReports%s {
            totalCount
            edges {
                cursor
                node {
                    id
                    date
                    published
                    title
                    body
                    receivedBenefit
                    providedBenefit
                    ourParticipants
                    otherParticipants
                    isDraft
                    extra
                    author {
                        id
                        firstName
                        lastName
                        hasCollidingName
                        totalReports
                        extra
                    }
                }
            }
            pageInfo {
                hasPreviousPage
                hasNextPage
                startCursor
                endCursor
            }
        }
    }
    """
    yield template % ''
    yield template % '(sort:{sort})'.format(sort=sort)
    yield template % '(sort:{sort}, reversed:true)'.format(sort=sort)
    yield template % '(sort:{sort}, reversed:false)'.format(sort=sort)

