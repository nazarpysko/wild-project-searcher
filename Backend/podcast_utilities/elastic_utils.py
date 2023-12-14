from elasticsearch import Elasticsearch
from utilities import SingletonMeta
from constants import ELASTIC_USERNAME, ELASTIC_HOST, CERTIFICATE_PATH, ELASTIC_INDEXES, INDEX_MAPPINGS
from podcast_utilities.transformer_model import Model

class Elastic(metaclass=SingletonMeta):
    def __init__(self, password, clean=False):
        self.es = Elasticsearch(
            ELASTIC_HOST,
            basic_auth=(ELASTIC_USERNAME, password),
            ca_certs=CERTIFICATE_PATH
        )

        self.model = Model()

        if clean:
            self._remove_indexes()
            self._create_indexes()


    # Returns true if a connection has been established
    def check_connection(self):
        return self.es.ping()

    def _remove_indexes(self):
        for index_name in ELASTIC_INDEXES:
            try:
                self.es.indices.delete(index=index_name)
            except:
                pass

    def _create_indexes(self):
        for index_name in ELASTIC_INDEXES:
            try:
                self.es.indices.create(index=index_name, mappings=INDEX_MAPPINGS[index_name])
            except:
                pass

    # Adds a record style list into an index
    def feed_records_to_index(self, record_list, index):
        for record in record_list:
            self.es.index(index=index, document=record, id=record["id"])

    # Queries the database with some keyword
    # Returns the 10 most related podcasts
    def query_model(self, input_keyword):
        vector = self.model.feed_text(input_keyword)
        query = {
            "field": "text_vector",
            "query_vector": vector,
            "k": 10,
            "num_candidates": 500
        }
        res = self.es.knn_search(index="videos",
                                 knn=query,
                                 source=["video_id", "text"])

        return res["hits"]["hits"]

    # Returns the number of documents on the database on a discrete index
    def get_num_documents(self, index):
        return self.es.count(index=index)