import arrow

from openlobby.core.models import Report, User


authors = [
    {
        "id": 1,
        "username": "wolf",
        "first_name": "Winston",
        "last_name": "Wolfe",
        "is_author": True,
        "extra": {"movies": 1},
    },
    {
        "id": 2,
        "username": "shaun",
        "first_name": "Shaun",
        "last_name": "Sheep",
        "is_author": True,
    },
    {
        "id": 3,
        "username": "sponge",
        "first_name": "Spongebob",
        "last_name": "Squarepants",
        "is_author": True,
    },
]

reports = [
    {
        "id": 1,
        "date": arrow.get(2018, 1, 1).datetime,
        "published": arrow.get(2018, 1, 2).datetime,
        "edited": arrow.get(2018, 1, 2, 3).datetime,
        "title": "The Fellowship of the Ring",
        "body": "Long story short: we got the Ring!",
        "received_benefit": "The Ring",
        "provided_benefit": "",
        "our_participants": "Frodo, Gandalf",
        "other_participants": "Saruman",
    },
    {
        "id": 2,
        "date": arrow.get(2018, 1, 3).datetime,
        "published": arrow.get(2018, 1, 4).datetime,
        "edited": arrow.get(2018, 1, 4, 5).datetime,
        "title": "The Two Towers",
        "body": "Another long story.",
        "received_benefit": "Mithrill Jacket",
        "provided_benefit": "",
        "our_participants": "Frodo, Gimli, Legolas",
        "other_participants": "Saruman, Sauron",
        "extra": {"rings": 1},
    },
    {
        "id": 3,
        "date": arrow.get(2018, 1, 5).datetime,
        "published": arrow.get(2018, 1, 6).datetime,
        "edited": arrow.get(2018, 1, 6, 7).datetime,
        "title": "The Return of the King",
        "body": "Aragorn is the King. And we have lost the Ring.",
        "received_benefit": "",
        "provided_benefit": "The Ring",
        "our_participants": "Aragorn",
        "other_participants": "Sauron",
    },
    {
        "id": 4,
        "date": arrow.get(2018, 1, 7).datetime,
        "published": arrow.get(2018, 1, 8).datetime,
        "edited": arrow.get(2018, 1, 8, 9).datetime,
        "title": "The Silmarillion",
        "body": "Not finished yet.",
        "received_benefit": "",
        "provided_benefit": "",
        "our_participants": "",
        "other_participants": "",
        "is_draft": True,
    },
    {
        "id": 5,
        "date": arrow.get(2018, 1, 9).datetime,
        "published": arrow.get(2018, 1, 10).datetime,
        "edited": arrow.get(2018, 1, 10, 11).datetime,
        "title": "The Hobbit",
        "body": "Work in progress...",
        "received_benefit": "",
        "provided_benefit": "",
        "our_participants": "",
        "other_participants": "",
        "is_draft": True,
    },
    {
        "id": 6,
        "superseded_by_id": 2,
        "date": arrow.get(2018, 1, 3).datetime,
        "published": arrow.get(2018, 1, 4).datetime,
        "edited": arrow.get(2018, 2, 1).datetime,
        "title": "The Two Towers",
        "body": "Another long story in progress.",
        "received_benefit": "Mithrill Jacket",
        "provided_benefit": "The Ring",
        "our_participants": "Frodo, Gimli, Legolas",
        "other_participants": "Saruman, Sauron",
        "extra": {"rings": 2},
    },
    {
        "id": 7,
        "superseded_by_id": 2,
        "date": arrow.get(2018, 1, 3).datetime,
        "published": arrow.get(2018, 1, 4).datetime,
        "edited": arrow.get(2018, 2, 5).datetime,
        "title": "The Towels",
        "body": "What am I doing?",
        "received_benefit": "Jacket",
        "provided_benefit": "The Ringo",
        "our_participants": "Ringo Starr",
        "other_participants": "",
        "extra": {"rings": 1},
    },
    {
        "id": 8,
        "superseded_by_id": 1,
        "date": arrow.get(2018, 1, 1).datetime,
        "published": arrow.get(2018, 1, 2).datetime,
        "edited": arrow.get(2018, 1, 3).datetime,
        "title": "The Fellowship of the Ringing Bell",
        "body": "The bell is ringing!",
        "received_benefit": "bell",
        "provided_benefit": "noise",
        "our_participants": "",
        "other_participants": "",
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
    Report.objects.create(author=author2, **reports[5])
    Report.objects.create(author=author2, **reports[6])
    Report.objects.create(author=author1, **reports[7])


def prepare_author():
    User.objects.create(**authors[0])


def prepare_report(is_draft=False):
    author = User.objects.create(**authors[0])
    Report.objects.create(author=author, is_draft=is_draft, **reports[0])
