import re

from .settings import ES_INDEX
from .documents import all_documents


class IndexAlreadyExistsError(Exception):
    pass


class AliasAlreadyExistsError(Exception):
    pass


INDEX_SETTINGS = {
    'settings': {
        'analysis': {
            'filter': {
                'czech_stop': {
                    'type': 'stop',
                    'stopwords': '_czech_',
                },
                'czech_stemmer': {
                    'type': 'stemmer',
                    'language': 'czech',
                },
                'cs_CZ': {
                    'type': 'hunspell',
                    'locale': 'cs_CZ',
                    'dedup': True,
                },
                'czech_synonym': {
                    'type': 'synonym',
                    'synonyms_path': 'analysis/cs_CZ/synonym.txt',
                },
            },
            'analyzer': {
                'czech': {
                    'tokenizer': 'standard',
                    'filter': [
                        'icu_folding',
                        'lowercase',
                        'czech_synonym',
                        'czech_stop',
                        'czech_stemmer',
                        'cs_CZ',
                    ]
                }
            }
        }
    }
}


def bootstrap_es(es):
    if es.indices.exists(ES_INDEX):
        return

    print('Bootstrapping index and documents.')
    init_alias(es, ES_INDEX)


def init_documents(es, index):
    """Initializes all documents."""
    for doc in all_documents:
        doc.init(index=index, using=es)


def get_new_index_version(index):
    """Returns name of new version of index."""
    m = re.match(r'(.+)_v([\d]+)$', index)
    if not m:
        raise ValueError('Cannot get version from index name "{}"'.format(index))

    alias = m.group(1)
    version = m.group(2)
    new_version = int(version) + 1
    return '{}_v{}'.format(alias, new_version)


def create_index(es, name):
    """Creates index with INDEX_SETTINGS and all documents (mappings)."""
    if es.indices.exists(name):
        raise IndexAlreadyExistsError('Index "{}" already exists.'.format(name))

    es.indices.create(name, body=INDEX_SETTINGS)
    init_documents(es, name)


def init_alias(es, alias):
    """Initializes alias for the first time. Creates index v1 for alias."""
    if es.indices.exists(alias):
        raise AliasAlreadyExistsError('Alias "{}" already exists.'.format(alias))

    index = '{}_v1'.format(alias)
    create_index(es, index)
    es.indices.put_alias(name=alias, index=index)


def reindex(es, alias):
    """
    Reindexes index by alias into new version (with actual index settings and
    mappings definitions) and switches alias.
    """
    response = es.indices.get_alias(alias)
    source = list(response.keys())[0]

    dest = get_new_index_version(source)
    create_index(es, dest)

    es.reindex(body={
        'source': {'index': source},
        'dest': {'index': dest},
    })

    es.indices.update_aliases(body={
        'actions': [
            {'remove': {'index': source, 'alias': alias}},
            {'add': {'index': dest, 'alias': alias}},
        ],
    })
