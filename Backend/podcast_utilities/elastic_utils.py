from elasticsearch import Elasticsearch

import constants
from utilities import SingletonMeta
from constants import ELASTIC_USERNAME, ELASTIC_HOST, ELASTIC_INDEXES, INDEX_MAPPINGS
from podcast_utilities.transformer_model import Model


def _format_results(result_hits):
    retVal = {}
    for result in result_hits:
        info = result["_source"]
        id = info["video_id"]
        transcription = {
            "transcription": info["text"],
            "timestamp": info["start"]
        }
        if id in retVal:
            retVal[id]["transcriptions"].append(transcription)
        else:
            retVal[id] = {
                "video_id": info["video_id"],
                "title": info["title"],
                "transcriptions": [transcription],
            }

    return list(retVal.values())


class Elastic(metaclass=SingletonMeta):
    def __init__(self, password, certificate_path, clean=False):
        self.es = Elasticsearch(
            ELASTIC_HOST,
            basic_auth=(ELASTIC_USERNAME, password),
            ca_certs=certificate_path
        )

        self.model = Model()

        if clean:
            self._remove_indexes()
            self._create_indexes()

    # Returns true if a connection has been established
    def check_connection(self):
        ping_response = self.es.ping()
        try:
            extra_info = self.es.info()
        except Exception as exc:
            extra_info = exc

        return ping_response, extra_info

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
    def feed_records_to_index(self, record_list, index, index_id="id"):
        for record in record_list:
            self.es.index(index=index, document=record, id=record[index_id])

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
                                 source=["video_id", "text", "start", "title"])

        return _format_results(res["hits"]["hits"])

    # Returns the number of documents on the database on a discrete index
    def get_num_documents(self):
        retVal = {}
        for index in constants.ELASTIC_INDEXES:
            retVal[index] = self.es.count(index=index)["count"]

        return retVal

    def create_snapshot_repository(self, name):
        self.es.snapshot.create_repository(name=name, settings={"location": "/mnt/backups/test"}, type="fs")

    def create_snapshot(self, rep_name, snap_name):
        self.es.snapshot.create(repository=rep_name, snapshot=snap_name)
