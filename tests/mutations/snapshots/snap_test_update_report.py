# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_unauthorized 1'] = {
    'data': {
        'updateReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'User must be logged in to perform this mutation.',
            'path': [
                'updateReport'
            ]
        }
    ]
}

snapshots['test_not_author 1'] = {
    'data': {
        'updateReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'Viewer is not the Author of this Report or Report does not exist.',
            'path': [
                'updateReport'
            ]
        }
    ]
}

snapshots['test_report_does_not_exist 1'] = {
    'data': {
        'updateReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'Viewer is not the Author of this Report or Report does not exist.',
            'path': [
                'updateReport'
            ]
        }
    ]
}

snapshots['test_update_published_with_draft 1'] = {
    'data': {
        'updateReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'You cannot update published Report with draft.',
            'path': [
                'updateReport'
            ]
        }
    ]
}

snapshots['test_update_draft_with_draft 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 0
                },
                'body': 'Rewrited',
                'date': '2018-03-03 00:00:00+00:00',
                'edited': '2018-01-02 05:50:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjY2Ng==',
                'isDraft': True,
                'otherParticipants': 'grandchilds',
                'ourParticipants': 'kids',
                'providedBenefit': 'water',
                'published': '2018-01-02 05:50:00+00:00',
                'receivedBenefit': 'cake',
                'title': 'New title'
            }
        }
    }
}

snapshots['test_update_draft_with_published 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'Rewrited',
                'date': '2018-03-03 00:00:00+00:00',
                'edited': '2018-01-02 05:50:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjY2Ng==',
                'isDraft': False,
                'otherParticipants': 'grandchilds',
                'ourParticipants': 'kids',
                'providedBenefit': 'water',
                'published': '2018-01-02 05:50:00+00:00',
                'receivedBenefit': 'cake',
                'title': 'New title'
            }
        }
    }
}

snapshots['test_update_published_with_published 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'Rewrited',
                'date': '2018-03-03 00:00:00+00:00',
                'edited': '2018-01-02 05:50:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjY2Ng==',
                'isDraft': False,
                'otherParticipants': 'grandchilds',
                'ourParticipants': 'kids',
                'providedBenefit': 'water',
                'published': '2018-01-02 00:00:00+00:00',
                'receivedBenefit': 'cake',
                'title': 'New title'
            }
        }
    }
}

snapshots['test_input_sanitization 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'some link in body',
                'date': '2018-03-03 00:00:00+00:00',
                'edited': '2018-01-02 05:50:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjY2Ng==',
                'isDraft': False,
                'otherParticipants': 'you!',
                'ourParticipants': 'me, myself',
                'providedBenefit': 'tea',
                'published': '2018-01-02 00:00:00+00:00',
                'receivedBenefit': 'coffee',
                'title': 'No tags'
            }
        }
    }
}

snapshots['test_update_draft_with_draft__late_edit 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 0
                },
                'body': 'Rewrited',
                'date': '2018-03-03 00:00:00+00:00',
                'edited': '2018-01-02 06:10:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjY2Ng==',
                'isDraft': True,
                'otherParticipants': 'grandchilds',
                'ourParticipants': 'kids',
                'providedBenefit': 'water',
                'published': '2018-01-02 06:10:00+00:00',
                'receivedBenefit': 'cake',
                'title': 'New title'
            }
        }
    }
}

snapshots['test_update_draft_with_published__late_edit 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'Rewrited',
                'date': '2018-03-03 00:00:00+00:00',
                'edited': '2018-01-02 06:10:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjY2Ng==',
                'isDraft': False,
                'otherParticipants': 'grandchilds',
                'ourParticipants': 'kids',
                'providedBenefit': 'water',
                'published': '2018-01-02 06:10:00+00:00',
                'receivedBenefit': 'cake',
                'title': 'New title'
            }
        }
    }
}

snapshots['test_update_draft_with_draft 2'] = [
    {
        'author_id': 42,
        'body': 'Rewrited',
        'date': '2018-03-03T00:00:00+00:00',
        'edited': '2018-01-02T05:50:00+00:00',
        'extra': None,
        'id': 666,
        'is_draft': True,
        'other_participants': 'grandchilds',
        'our_participants': 'kids',
        'provided_benefit': 'water',
        'published': '2018-01-02T05:50:00+00:00',
        'received_benefit': 'cake',
        'superseded_by_id': None,
        'title': 'New title'
    }
]

snapshots['test_update_draft_with_draft__late_edit 2'] = [
    {
        'author_id': 42,
        'body': 'Rewrited',
        'date': '2018-03-03T00:00:00+00:00',
        'edited': '2018-01-02T06:10:00+00:00',
        'extra': None,
        'id': 666,
        'is_draft': True,
        'other_participants': 'grandchilds',
        'our_participants': 'kids',
        'provided_benefit': 'water',
        'published': '2018-01-02T06:10:00+00:00',
        'received_benefit': 'cake',
        'superseded_by_id': None,
        'title': 'New title'
    }
]

snapshots['test_update_draft_with_published 2'] = [
    {
        'author_id': 42,
        'body': 'Rewrited',
        'date': '2018-03-03T00:00:00+00:00',
        'edited': '2018-01-02T05:50:00+00:00',
        'extra': None,
        'id': 666,
        'is_draft': False,
        'other_participants': 'grandchilds',
        'our_participants': 'kids',
        'provided_benefit': 'water',
        'published': '2018-01-02T05:50:00+00:00',
        'received_benefit': 'cake',
        'superseded_by_id': None,
        'title': 'New title'
    }
]

snapshots['test_update_draft_with_published__late_edit 2'] = [
    {
        'author_id': 42,
        'body': 'Rewrited',
        'date': '2018-03-03T00:00:00+00:00',
        'edited': '2018-01-02T06:10:00+00:00',
        'extra': None,
        'id': 666,
        'is_draft': False,
        'other_participants': 'grandchilds',
        'our_participants': 'kids',
        'provided_benefit': 'water',
        'published': '2018-01-02T06:10:00+00:00',
        'received_benefit': 'cake',
        'superseded_by_id': None,
        'title': 'New title'
    }
]

snapshots['test_update_published_with_published 2'] = [
    {
        'author_id': 42,
        'body': 'Rewrited',
        'date': '2018-03-03T00:00:00+00:00',
        'edited': '2018-01-02T05:50:00+00:00',
        'extra': None,
        'id': 666,
        'is_draft': False,
        'other_participants': 'grandchilds',
        'our_participants': 'kids',
        'provided_benefit': 'water',
        'published': '2018-01-02T00:00:00+00:00',
        'received_benefit': 'cake',
        'superseded_by_id': None,
        'title': 'New title'
    }
]

snapshots['test_update_published_with_published__late_edit 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'Rewrited',
                'date': '2018-03-03 00:00:00+00:00',
                'edited': '2018-01-02 06:10:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjY2Ng==',
                'isDraft': False,
                'otherParticipants': 'grandchilds',
                'ourParticipants': 'kids',
                'providedBenefit': 'water',
                'published': '2018-01-02 00:00:00+00:00',
                'receivedBenefit': 'cake',
                'title': 'New title'
            }
        }
    }
}

snapshots['test_update_published_with_published__late_edit 2'] = {
    'author_id': 42,
    'body': 'Rewrited',
    'date': '2018-03-03T00:00:00+00:00',
    'edited': '2018-01-02T06:10:00+00:00',
    'extra': None,
    'id': 666,
    'is_draft': False,
    'other_participants': 'grandchilds',
    'our_participants': 'kids',
    'provided_benefit': 'water',
    'published': '2018-01-02T00:00:00+00:00',
    'received_benefit': 'cake',
    'superseded_by_id': None,
    'title': 'New title'
}

snapshots['test_input_sanitization 2'] = [
    {
        'author_id': 42,
        'body': 'some link in body',
        'date': '2018-03-03T00:00:00+00:00',
        'edited': '2018-01-02T05:50:00+00:00',
        'extra': None,
        'id': 666,
        'is_draft': False,
        'other_participants': 'you!',
        'our_participants': 'me, myself',
        'provided_benefit': 'tea',
        'published': '2018-01-02T00:00:00+00:00',
        'received_benefit': 'coffee',
        'superseded_by_id': None,
        'title': 'No tags'
    }
]

snapshots['test_update_published_with_published__late_edit 3'] = {
    'author_id': 42,
    'body': 'Previous body.',
    'date': '2018-01-01T00:00:00+00:00',
    'edited': '2018-01-02T05:00:00+00:00',
    'extra': None,
    'id': '__STRIPPED__',
    'is_draft': False,
    'other_participants': 'grandma',
    'our_participants': 'grandpa',
    'provided_benefit': 'old tea',
    'published': '2018-01-02T00:00:00+00:00',
    'received_benefit': 'old coffee',
    'superseded_by_id': 666,
    'title': 'Original'
}
