import json
import os

from constants import (PASSWORD_PATH,
                       CERTIFICATE_PATH,
                       MESSAGE_ES_NOT_CONNECTED,
                       INITIAL_DOCUMENTS_PATH,
                       ELASTIC_INDEXES,
                       MAX_TRIES)
from podcast_utilities.elastic_utils import Elastic
from utilities import wait_for_file


def init_documents():
    files = os.listdir(INITIAL_DOCUMENTS_PATH)
    for file_name in files:
        file_read_path = INITIAL_DOCUMENTS_PATH + "/" + file_name
        with open(file_read_path, "r", encoding='utf-8') as file:
            if file_name.split('.')[0].split('_')[-1] == "text":
                index = ELASTIC_INDEXES[0]
                index_id = "video_id"
            else:
                index = ELASTIC_INDEXES[1]
                index_id = "id"

            print("Uploading:", file_name, "to elastic search at index", index)

            file_json = json.loads(file.read())
            es.feed_records_to_index(file_json, index, index_id)


if __name__ == "__main__":
    if not wait_for_file(PASSWORD_PATH, "Password", MAX_TRIES, 10):
        exit(1)

    if not wait_for_file(CERTIFICATE_PATH, "Certificate", MAX_TRIES, 10):
        exit(1)

    with open(PASSWORD_PATH, mode="r") as file:
        password = file.read()

    es = Elastic(password, CERTIFICATE_PATH)
    ok, why = es.check_connection()

    if not ok:
        print(MESSAGE_ES_NOT_CONNECTED + " " + str(why))

    else:
        es.create_indexes()
        docs = es.get_num_documents()
        values = list(docs.values())
        print("There are", values[0], "in one index and", values[1], "in the other")
        if values[1] == 0:
            init_documents()
