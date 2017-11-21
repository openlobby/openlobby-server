import json

from .settings import ES_INDEX
from .documents import UserDoc, ReportDoc, LoginAttemptDoc


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
                }
            },
            'analyzer': {
                'czech': {
                    'tokenizer': 'standard',
                    'filter': [
                        'icu_folding',
                        'lowercase',
                        'czech_stop',
                        'czech_stemmer',
                        'cs_CZ',
                    ]
                }
            }
        }
    }
}


def bootstrap_es(client):
    if client.indices.exists(ES_INDEX):
        return

    print('Bootstrapping index and documents.')

    client.indices.create(ES_INDEX, body=json.dumps(INDEX_SETTINGS))

    UserDoc.init(using=client)
    ReportDoc.init(using=client)
    LoginAttemptDoc.init(using=client)
