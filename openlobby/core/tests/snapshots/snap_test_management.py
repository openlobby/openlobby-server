# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_index__check_analysis_settings 1'] = {
    'analyzer': {
        'czech': {
            'filter': [
                'icu_folding',
                'lowercase',
                'czech_synonym',
                'czech_stop',
                'czech_stemmer',
                'cs_CZ'
            ],
            'tokenizer': 'standard'
        }
    },
    'filter': {
        'cs_CZ': {
            'dedup': 'true',
            'locale': 'cs_CZ',
            'type': 'hunspell'
        },
        'czech_stemmer': {
            'language': 'czech',
            'type': 'stemmer'
        },
        'czech_stop': {
            'stopwords': '_czech_',
            'type': 'stop'
        },
        'czech_synonym': {
            'synonyms_path': 'analysis/cs_CZ/synonym.txt',
            'type': 'synonym'
        }
    }
}

snapshots['test_create_index__check_mappings 1'] = {
    'mappings': {
        'report': {
            'properties': {
                'author_id': {
                    'type': 'keyword'
                },
                'body': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'date': {
                    'type': 'date'
                },
                'extra': {
                    'type': 'object'
                },
                'other_participants': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'our_participants': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'provided_benefit': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'published': {
                    'type': 'date'
                },
                'received_benefit': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'title': {
                    'analyzer': 'czech',
                    'type': 'text'
                }
            }
        },
        'session': {
            'properties': {
                'expiration': {
                    'type': 'integer'
                },
                'user_id': {
                    'type': 'keyword'
                }
            }
        },
        'user': {
            'properties': {
                'email': {
                    'type': 'keyword'
                },
                'extra': {
                    'type': 'object'
                },
                'name': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'openid_uid': {
                    'type': 'keyword'
                }
            }
        }
    }
}

snapshots['test_init_alias 1'] = {
    'mappings': {
        'report': {
            'properties': {
                'author_id': {
                    'type': 'keyword'
                },
                'body': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'date': {
                    'type': 'date'
                },
                'extra': {
                    'type': 'object'
                },
                'other_participants': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'our_participants': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'provided_benefit': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'published': {
                    'type': 'date'
                },
                'received_benefit': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'title': {
                    'analyzer': 'czech',
                    'type': 'text'
                }
            }
        },
        'session': {
            'properties': {
                'expiration': {
                    'type': 'integer'
                },
                'user_id': {
                    'type': 'keyword'
                }
            }
        },
        'user': {
            'properties': {
                'email': {
                    'type': 'keyword'
                },
                'extra': {
                    'type': 'object'
                },
                'name': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'openid_uid': {
                    'type': 'keyword'
                }
            }
        }
    }
}

snapshots['test_reindex__check_new_index 1'] = {
    'mappings': {
        'report': {
            'properties': {
                'author_id': {
                    'type': 'keyword'
                },
                'body': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'date': {
                    'type': 'date'
                },
                'extra': {
                    'type': 'object'
                },
                'other_participants': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'our_participants': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'provided_benefit': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'published': {
                    'type': 'date'
                },
                'received_benefit': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'title': {
                    'analyzer': 'czech',
                    'type': 'text'
                }
            }
        },
        'session': {
            'properties': {
                'expiration': {
                    'type': 'integer'
                },
                'user_id': {
                    'type': 'keyword'
                }
            }
        },
        'user': {
            'properties': {
                'email': {
                    'type': 'keyword'
                },
                'extra': {
                    'type': 'object'
                },
                'name': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'openid_uid': {
                    'type': 'keyword'
                }
            }
        }
    }
}

snapshots['test_init_documents 1'] = {
    'mappings': {
        'report': {
            'properties': {
                'author_id': {
                    'type': 'keyword'
                },
                'body': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'date': {
                    'type': 'date'
                },
                'extra': {
                    'type': 'object'
                },
                'other_participants': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'our_participants': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'provided_benefit': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'published': {
                    'type': 'date'
                },
                'received_benefit': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'title': {
                    'analyzer': 'czech',
                    'type': 'text'
                }
            }
        },
        'session': {
            'properties': {
                'expiration': {
                    'type': 'integer'
                },
                'user_id': {
                    'type': 'keyword'
                }
            }
        },
        'user': {
            'properties': {
                'email': {
                    'type': 'keyword'
                },
                'extra': {
                    'type': 'object'
                },
                'name': {
                    'analyzer': 'czech',
                    'type': 'text'
                },
                'openid_uid': {
                    'type': 'keyword'
                }
            }
        }
    }
}
