from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import argparse
import constants
from podcast_utilities.elastic_utils import Elastic
from podcast_utilities.file_utils import transform_json
from podcast_utilities.transformer_model import Model
from flask_cors import CORS

parser_podcast = reqparse.RequestParser()
parser_podcast.add_argument('video_id', required=True, location='form')

parser_searcher = reqparse.RequestParser()
parser_searcher.add_argument('query', required=True, location='form')

# Document operations API
class Podcast(Resource):
    def put(self):
        # TODO: Add conflict when already on elastic database
        args = parser_podcast.parse_args()
        json_transcription, _ = transform_json("./documents/test/my_transcript_10_videos.json")
        formatted_transcription = model.feed_json(json_transcription)
        es.feed_records_to_index(formatted_transcription, constants.ELASTIC_INDEXES[1])
        return {'video_id': json_transcription[0]['video_id'], 'title': json_transcription[0]['title']}, constants.HTTP_OK

    def delete(self):
        # TODO: Delete from elastic database
        # Error : abort(constants.HTTP_NOT_FOUND, message="podcast not found")
        return "test", constants.HTTP_OK


# Query operations API
class Searcher(Resource):
    def put(self):
        args = parser_searcher.parse_args()
        print("Received:", args['query'])
        data = es.query_model(args['query'])
        print(data)
        return data

    def get(self):
        retval = []
        for index in constants.ELASTIC_INDEXES:
            retval.append(str(es.get_num_documents(index)))

        return retval

# Debug operation API
class Debug(Resource):
    def get(self, action):
        if action == "clean":
            es._remove_indexes()
            es._create_indexes()

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

    else:
        print(args)
        es = Elastic(args.elastic_password, args.clean_start)
        if not es.check_connection():
            print("Some error curred while connecting to elastic search, try again")
        else:
            print("Connected successfully to elastic search!!")
            model = Model()

            # Creates a Flask Application
            app = Flask("PodcastAPI")
            CORS(app)
            api = Api(app)

            # Defines the endpoints
            api.add_resource(Podcast,   '/api/podcast')
            api.add_resource(Searcher,  '/api/search')
            api.add_resource(Debug,     '/api/debug/<action>') # Remove before submitting

            # Starts the API server
            app.run()
