from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api, reqparse
import constants
from podcast_utilities.elastic_utils import Elastic
from podcast_utilities.file_utils import transform_json
from podcast_utilities.transformer_model import Model
from flask_cors import CORS
from utilities import wait_for_file


def check_es_connection(es: Elastic):
    if es is None:
        return False, "No Elastic object created"

    ok, why = es.check_connection()
    return ok, str(why)


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
                  message=constants.MESSAGE_ES_NOT_CONNECTED + " " + why)

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
                  message=constants.MESSAGE_ES_NOT_CONNECTED + " " + why)

        # Error : abort(constants.HTTP_NOT_FOUND, message="podcast not found")
        return jsonify({'message': 'Yet to create'}), constants.HTTP_ERROR_NOT_IMPLEMENTED


# Query operations API
class Searcher(Resource):
    def get(self):
        ok, why = check_es_connection(es)
        if not ok:
            abort(constants.HTTP_ERROR_SERVICE_UNAVAILABLE,
                  message=constants.MESSAGE_ES_NOT_CONNECTED + " " + why)

        query = request.args.get('query')
        print("Received query:", query)
        data = es.query_model(query)
        return jsonify(data)


es = None
model = Model()

# Creates a Flask Application
app = Flask("PodcastAPI")
CORS(app)
api = Api(app)

# Defines the endpoints
api.add_resource(Podcast, '/api/podcast')
api.add_resource(Searcher, '/api/search')

if __name__ == '__main__':
    if not wait_for_file(constants.PASSWORD_PATH, "Password", constants.MAX_TRIES, 10):
        exit(1)

    if not wait_for_file(constants.CERTIFICATE_PATH, "Certificate", constants.MAX_TRIES, 10):
        exit(1)

    with open(constants.PASSWORD_PATH, "r") as file:
        password = file.read()

    es = Elastic(password, constants.CERTIFICATE_PATH)
    ok, why = es.check_connection()

    if not ok:
        print(constants.MESSAGE_ES_NOT_CONNECTED + "\n" + str(why))
    else:
        print(constants.MESSAGE_ES_CONNECTED)

    # Starts the API server
    app.run()
