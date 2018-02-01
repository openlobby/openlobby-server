import arrow

from openlobby.core.models import Report, User


authors = [
    {
        'id': 1,
        'username': 'Wolf',
        'openid_uid': 'Wolf',
        'first_name': 'Winston',
        'last_name': 'Wolfe',
        'is_author': True,
        'extra': {'movies': 1},
    },
    {
        'id': 2,
        'username': 'sponge',
        'openid_uid': 'sponge',
        'first_name': 'Spongebob',
        'last_name': 'Squarepants',
        'is_author': True,
    },
    {
        'id': 3,
        'username': 'shaun',
        'openid_uid': 'shaun',
        'first_name': 'Shaun',
        'last_name': 'Sheep',
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
        'date': arrow.get(2018, 1, 5).datetime,
        'published': arrow.get(2018, 1, 10).datetime,
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
        'date': arrow.get(2018, 1, 7).datetime,
        'published': arrow.get(2018, 1, 8).datetime,
        'title': 'The Return of the King',
        'body': 'Aragorn is the King. And we have lost the Ring.',
        'received_benefit': '',
        'provided_benefit': 'The Ring',
        'our_participants': 'Aragorn',
        'other_participants': 'Sauron',
    },
]


def prepare_reports():
    author1 = User.objects.create(**authors[0])
    author2 = User.objects.create(**authors[1])
    Report.objects.create(author=author1, **reports[0])
    Report.objects.create(author=author2, **reports[1])
    Report.objects.create(author=author1, **reports[2])


def prepare_report():
    author = User.objects.create(**authors[0])
    Report.objects.create(author=author, **reports[0])


def prepare_authors():
    for author in authors:
        User.objects.create(**author)
