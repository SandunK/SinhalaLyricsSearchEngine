from elasticsearch import Elasticsearch
import json


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def create_index(es_object, index_name):
    with open("settings.json") as settings:
        settings_data = json.load(settings)

    with open("mapping.json", encoding="utf8") as mapping:
        mapping_data = json.load(mapping)

    created = False
    # index settings
    settings = {
        "settings": settings_data,
        "mappings": mapping_data
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Index Created ...')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, id, record):
    try:
        outcome = elastic_object.index(index=index_name, id=id, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
