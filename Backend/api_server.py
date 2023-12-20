import json
import os

from flask import Flask, jsonify, abort
from flask_restful import Resource, Api, reqparse
import argparse
import constants
from podcast_utilities.elastic_utils import Elastic
from podcast_utilities.file_utils import transform_json
from podcast_utilities.transformer_model import Model
from flask_cors import CORS


def check_es_connection(es: Elastic):
    return not(es is None or not es.check_connection()[0])


def init_documents():
    files = os.listdir(constants.INITIAL_DOCUMENTS_PATH)
    for file_name in files:
        file_read_path = constants.INITIAL_DOCUMENTS_PATH + "/" + file_name
        with open(file_read_path, "r", encoding='utf-8') as file:
            if file_name.split('.')[0].split('_')[-1] == "text":
                index = constants.ELASTIC_INDEXES[0]
                index_id = "video_id"
            else:
                index = constants.ELASTIC_INDEXES[1]
                index_id = "id"

            print("Uploading:", file_name, "to elastic search at index", index)

            file_json = json.loads(file.read())
            es.feed_records_to_index(file_json, index, index_id)


parser_podcast = reqparse.RequestParser()
parser_podcast.add_argument('video_id', required=True, location='form')

parser_searcher = reqparse.RequestParser()
parser_searcher.add_argument('query', required=True, location='form')


# Document operations API
class Podcast(Resource):
    def put(self):
        # TODO: Add conflict when already on elastic database
        ok, why = check_es_connection(es)
        if not ok:
            abort(constants.HTTP_ERROR_SERVICE_UNAVAILABLE,
                  message=constants.HTTP_MESSAGE_ES_NOT_CONNECTED + " " + why)

        json_transcription, _ = transform_json("./documents/test/my_transcript_10_videos.json")
        formatted_transcription = model.feed_json(json_transcription)
        es.feed_records_to_index(formatted_transcription, constants.ELASTIC_INDEXES[1])
        response = jsonify({'videos_added': len(json_transcription)})

        return response, constants.HTTP_OK

    def delete(self):
        # TODO: Delete from elastic database
        ok, why = check_es_connection(es)
        if not ok:
            abort(constants.HTTP_ERROR_SERVICE_UNAVAILABLE,
                  message=constants.HTTP_MESSAGE_ES_NOT_CONNECTED + " " + why)

        # Error : abort(constants.HTTP_NOT_FOUND, message="podcast not found")
        return jsonify({'message': 'Yet to create'}), constants.HTTP_ERROR_NOT_IMPLEMENTED


# Query operations API
class Searcher(Resource):
    def get(self, query):
        ok, why = check_es_connection(es)
        if not ok:
            abort(constants.HTTP_ERROR_SERVICE_UNAVAILABLE,
                  message=constants.HTTP_MESSAGE_ES_NOT_CONNECTED + " " + why)

        print("Received query:", query)
        data = es.query_model(args['query'])
        return jsonify(data), constants.HTTP_OK


es = None
model = Model()

# Creates a Flask Application
app = Flask("PodcastAPI")
CORS(app)
api = Api(app)

# Defines the endpoints
api.add_resource(Podcast,   '/api/podcast')
api.add_resource(Searcher,  '/api/search/<query>')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog=constants.PROGRAM_NAME,
        description=constants.PROGRAM_DESCRIPTION,
        epilog=constants.PROGRAM_EPILOG)

    arg_parser.add_argument('-v', '--version', action="store_true", help="Prints current version")
    arg_parser.add_argument('-ep', '--elastic-password', help="ElasticSearch server password")
    arg_parser.add_argument('-cs', '--clean-start', action="store_true", help="Starts the program like it would do the first time")

    args = arg_parser.parse_args()

    if args.version:
        print(constants.PROGRAM_NAME, "- Version:", constants.VERSION)
        exit()

    es = Elastic(args.elastic_password, clean=args.clean_start)
    ok, why = es.check_connection()
    if not ok:
        print(constants.HTTP_MESSAGE_ES_NOT_CONNECTED + " " + why)

    docs = es.get_num_documents()
    values = list(docs.values())
    if values[1] == 0:
        init_documents()

    # Starts the API server
    app.run()
