import pytest

from openlobby.management import (
    AliasAlreadyExistsError,
    IndexAlreadyExistsError,
    create_index,
    get_new_index_version,
    init_alias,
    init_documents,
    reindex,
)
from openlobby.documents import UserDoc


def test_create_index(es, index_name):
    create_index(es, index_name)
    assert es.indices.exists(index_name)


def test_create_index__already_exists(es, index_name):
    assert es.indices.create(index_name)
    with pytest.raises(IndexAlreadyExistsError):
        create_index(es, index_name)


def test_init_documents(es, index_name, snapshot):
    assert es.indices.create(index_name)
    init_documents(es, index_name)
    mappings = es.indices.get_mapping(index_name)
    snapshot.assert_match(mappings[index_name])


def test_create_index__check_analysis_settings(es, index_name, snapshot):
    create_index(es, index_name)
    settings = es.indices.get_settings(index=index_name)
    snapshot.assert_match(settings[index_name]['settings']['index']['analysis'])


def test_create_index__check_mappings(es, index_name, snapshot):
    create_index(es, index_name)
    mappings = es.indices.get_mapping(index_name)
    snapshot.assert_match(mappings[index_name])


@pytest.mark.parametrize('old, new', [
    ('foo_v1', 'foo_v2'),
    ('bar_v9', 'bar_v10'),
    ('two_words_v5', 'two_words_v6'),
])
def test_get_new_index_version(old, new):
    assert get_new_index_version(old) == new


def test_get_new_index_version__wrong_name():
    with pytest.raises(ValueError):
        get_new_index_version('foo')


def test_init_alias(es, index_name, snapshot):
    alias = index_name
    init_alias(es, alias)
    index = '{}_v1'.format(alias)
    assert es.indices.exists(alias)
    assert es.indices.exists(index)
    mappings = es.indices.get_mapping(index)
    snapshot.assert_match(mappings[index])


def test_init_alias__already_exists(es, index_name):
    alias = index_name
    init_alias(es, alias)
    with pytest.raises(AliasAlreadyExistsError):
        init_alias(es, alias)


def test_reindex__check_new_index(es, index_name, snapshot):
    alias = index_name
    init_alias(es, alias)
    reindex(es, alias)
    new_index = '{}_v2'.format(alias)
    assert es.indices.exists(new_index)
    mappings = es.indices.get_mapping(new_index)
    snapshot.assert_match(mappings[new_index])


def test_reindex__check_alias(es, index_name):
    alias = index_name
    init_alias(es, alias)
    reindex(es, alias)
    new_index = '{}_v2'.format(alias)
    assert es.indices.exists(alias)
    res = es.indices.get_alias(name=alias)
    assert res == {new_index: {'aliases': {alias: {}}}}


def test_reindex__with_some_data(es, index_name, snapshot):
    alias = index_name
    init_alias(es, alias)
    user = UserDoc(name='The Black Knight')
    user.save(using=es, index=alias)
    reindex(es, alias)
    new_user = UserDoc.get(id=user.meta.id, using=es, index=alias)
    assert new_user.name == 'The Black Knight'
