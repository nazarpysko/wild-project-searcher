# Server Configuration
HOST = "localhost"
PORT = 5000

# Elastic Configuration
ELASTIC_IP = "localhost"
ELASTIC_PORT = 9200
ELASTIC_USERNAME = "elastic"
CERTIFICATE_PATH = "documents/test/cert.crt"
ELASTIC_HOST = "https://" + ELASTIC_IP + ":" + str(ELASTIC_PORT) # Don't Change this
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

#HTTP Responses
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409

# Other
PROGRAM_NAME = "Podcast Transcription API Server"
PROGRAM_DESCRIPTION = ""
PROGRAM_EPILOG = ""
MODEL_NAME = "all-mpnet-base-v2"
VERSION = "1.0.0"
