# Server Configuration
HOST = "localhost"
PORT = 5000

# Elastic Configuration
ELASTIC_IP = "localhost"
ELASTIC_PORT = 9200
ELASTIC_USERNAME = "elastic"
CERTIFICATE_PATH = "es-config/certs/cert.crt"
PASSWORD_PATH = "run/secrets/es-password"
ELASTIC_HOST = "https://" + ELASTIC_IP + ":" + str(ELASTIC_PORT)  # Don't Change this
ELASTIC_INDEXES = ["full_transcription", "videos"]
INDEX_MAPPINGS = {
    "full_transcription": {
        "properties": {
            "title": {
                "type": "text"
            },
            "video_id": {
                "type": "text"
            },
            "start": {
                "type": "text"
            },
            "duration": {
                "type": "long"
            },
            "text": {
                "type": "text"
            },
            "text_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm"
            },
        }
    },
    "videos": {
        "properties": {
            "title": {
                "type": "text"
            },
            "video_id": {
                "type": "text"
            },
            "text": {
                "type": "text"
            },
            "text_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm"
            },
        }
    }
}

# HTTP Responses
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_ERROR_NOT_FOUND = 404
HTTP_ERROR_CONFLICT = 409
HTTP_ERROR_SERVICE_UNAVAILABLE = 503
HTTP_ERROR_NOT_IMPLEMENTED = 501

# Other
PROGRAM_NAME = "Podcast Transcription API Server"
PROGRAM_DESCRIPTION = ""
PROGRAM_EPILOG = ""
MODEL_NAME = "all-mpnet-base-v2"
VERSION = "1.0.0"
INITIAL_DOCUMENTS_PATH = "documents/initial/modeled"
MESSAGE_ES_NOT_CONNECTED = "Cannot make contact to the Elastic Search Server"
MESSAGE_ES_CONNECTED = "Connection to the Elastic Search Server successfully established"
MAX_TRIES = 30
