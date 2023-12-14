from elasticsearch import Elasticsearch
from utilities import SingletonMeta
from constants import ELASTIC_USERNAME, ELASTIC_HOST, CERTIFICATE_PATH, ELASTIC_INDEXES, INDEX_MAPPINGS
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
            retVal[id]["trancriptions"].append(transcription)
        else:
            retVal[id] = {
                "video_id": info["video_id"],
                "title": info["title"],
                "trancriptions": [transcription],
            }

    return list(retVal.values())

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
                                 source=["video_id", "text", "start", "title"])

        return _format_results(res["hits"]["hits"])
        # return res["hits"]["hits"]

    # Returns the number of documents on the database on a discrete index
    def get_num_documents(self, index):
        return self.es.count(index=index)


if __name__ == "__main__":
    print(_format_results([{"_index": "videos", "_id": "sKDk34V4rEQ32.2", "_score": 0.54544806, "_source": {"title": "\u00bfFingir\u00edas para conseguir un penalti importante? - Jordi Wild le pregunta a Ferran Torres", "video_id": "sKDk34V4rEQ", "text": "de simular el penalti de las protestas", "start": 32.2}}, {"_index": "videos", "_id": "sKDk34V4rEQ85.24", "_score": 0.5283436, "_source": {"title": "\u00bfFingir\u00edas para conseguir un penalti importante? - Jordi Wild le pregunta a Ferran Torres", "video_id": "sKDk34V4rEQ", "text": "penalti me la juego y tiro V\u00e1monos Yo", "start": 85.24}}, {"_index": "videos", "_id": "tBFERxANJQ829.48", "_score": 0.5188122, "_source": {"title": "CAE REDSYS Y ESPA\u00d1A SE QUEDA HORAS SIN PODER PAGAR CON TARJETA - Drama para muchos", "video_id": "tBFERxANJQ8", "text": "pagar con tarjeta de cr\u00e9dito o con", "start": 29.48}}, {"_index": "videos", "_id": "qkrxokg5JUI226.0", "_score": 0.50417453, "_source": {"title": "LAS PEL\u00cdCULAS FAVORITAS DE FERRAN TORRES - Jordi Wild emocionado y decepcionado a la vez", "video_id": "qkrxokg5JUI", "text": "s No sabr\u00eda decirte una eh No no t\u00edo", "start": 226.0}}, {"_index": "videos", "_id": "LTUUF_x5Ceg501.96", "_score": 0.5034765, "_source": {"title": "The Wild Project #244 ft Ferran Torres | C\u00f3mo pas\u00f3 de tocar fondo a convertirse en el Tibur\u00f3n", "video_id": "LTUUF_x5Ceg", "text": "entrenar con el con el filial y incluso", "start": 501.96}}, {"_index": "videos", "_id": "sKDk34V4rEQ28.96", "_score": 0.5031696, "_source": {"title": "\u00bfFingir\u00edas para conseguir un penalti importante? - Jordi Wild le pregunta a Ferran Torres", "video_id": "sKDk34V4rEQ", "text": "bar cardi de antes", "start": 28.96}}, {"_index": "videos", "_id": "tBFERxANJQ8134.64", "_score": 0.50168663, "_source": {"title": "CAE REDSYS Y ESPA\u00d1A SE QUEDA HORAS SIN PODER PAGAR CON TARJETA - Drama para muchos", "video_id": "tBFERxANJQ8", "text": "olvido de dejar la propina porque adem\u00e1s", "start": 134.64}}, {"_index": "videos", "_id": "gM2YLEsMpbI25.16", "_score": 0.5006254, "_source": {"title": "\u00bfREALMENTE HAS HECHO EL CURSO DE LLADOS? - Jordi pregunta a Ferran Torres y se lleva una sorpresa", "video_id": "gM2YLEsMpbI", "text": "una frase larga no cabe fortnite por", "start": 25.16}}, {"_index": "videos", "_id": "pH3hY6K_7gA295.84", "_score": 0.49869242, "_source": {"title": "Ferran Torres analiza sus inicios en el Bar\u00e7a, llegando a un club en muy malos momentos", "video_id": "pH3hY6K_7gA", "text": "como pueden ser ter stegen y sergi", "start": 295.84}}, {"_index": "videos", "_id": "LTUUF_x5Ceg682.399", "_score": 0.49562642, "_source": {"title": "The Wild Project #244 ft Ferran Torres | C\u00f3mo pas\u00f3 de tocar fondo a convertirse en el Tibur\u00f3n", "video_id": "LTUUF_x5Ceg", "text": "los fines de semana ve\u00edan a sus padres o", "start": 682.399}}]))