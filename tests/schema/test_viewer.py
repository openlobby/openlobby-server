import pytest

from openlobby.core.models import User


pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup():
    User.objects.create(id=1, is_author=True, username='a', openid_uid='TheWolf',
        first_name='Winston', last_name='Wolfe', email='winston@wolfe.com')


def test_unauthenticated(client, snapshot):
    res = client.post('/graphql', {'query': """
    query {
        viewer {
            openidUid
            firstName
            lastName
            email
        }
    }
    """})
    snapshot.assert_match(res.json())
