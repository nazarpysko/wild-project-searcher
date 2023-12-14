import json

def transform_json(file_path):
    with open(file_path, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)

    formatted = []
    full_documents = []

    for video in data:
        meta = video["metadata"]
        transcription = video["transcription"]
        full_transcription = ""

        for transcription_part in transcription:
            formatted.append(
                {
                    "id": str(meta["videoId"]) + str(transcription_part["start"]),
                    "title": meta["title"],
                    "video_id": meta["videoId"],
                    "text": transcription_part["text"],
                    "start": transcription_part["start"],
                    "duration": transcription_part["duration"],
                }
            )
            full_transcription += transcription_part["text"] + " "

        full_documents.append({
            "video_id": meta["videoId"],
            "title": meta["title"],
            "text": full_transcription,
        })

    return formatted, full_documents