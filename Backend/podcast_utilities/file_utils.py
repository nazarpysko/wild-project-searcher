import json
from youtube_transcript_api import YouTubeTranscriptApi
import os
import scrapetube
import tqdm


def transform_json(file_path):
    if isinstance(file_path, str):
        with open(file_path, "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
    else:
        data = file_path

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


def extract_video_id(video_id_or_url):
    # a youtube video id is 11 characters long
    # if the video id is longer than that, then it's a url
    if len(video_id_or_url) > 11:
        # it's a url
        # the video id is the last 11 characters
        return video_id_or_url[-11:]
    else:
        # it's a video id
        return video_id_or_url


def get_transcript(video_url_or_id):
    try:
        video_id = extract_video_id(video_url_or_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
        return transcript
    except Exception as e:
        print(f"Error: {e}")
        return None


def init_tmp_transcription():
  return {
      'text': '',
      'start': 0,
      'duration': 0
  }


def group_transcriptions(transcription, size=2, text_len=None):
    assert size != 0
    if size == 1:
        return transcription

    new_transcription = []
    tmp = init_tmp_transcription()
    current_size = 0

    for i, transcription in enumerate(transcription):
        tmp['text'] += transcription['text']
        tmp['duration'] += transcription['duration']
        current_size += 1

        if text_len is not None:
            if len(tmp['text']) > text_len:
                tmp['start'] = transcription['start']
                new_transcription.append(tmp)
                tmp = init_tmp_transcription()
            else:
                tmp['text'] += " "

        elif current_size >= size:
            tmp['start'] = transcription['start']
            new_transcription.append(tmp)
            tmp = init_tmp_transcription()
            size = 0

        else:
            tmp['text'] += " "

    return new_transcription


def transcribe_playlist(playlist_id, first_video=0, num_videos=10, group_size=2, len_size=None):
    videos = scrapetube.get_playlist(playlist_id)
    transcriptions = []

    for i, video in enumerate(videos):
        if i < first_video:
            continue

        title = video['title']['runs'][0]['text']
        videoId = video['videoId']
        transcription = get_transcript(videoId)
        transcription = group_transcriptions(transcription, group_size, len_size)
        transcriptions.append({
            "metadata": {
                "title": title,
                "videoId": videoId
            },
            "transcription": transcription
        })

        if i == first_video + num_videos - 1:
            break

    transformed = transform_json(transcriptions)

    path = f'../documents/initial/initial_transcriptions_{first_video}_{num_videos}.json'
    file_format = "x" if not os.path.exists(path) else "w"
    with open(path, file_format, encoding='utf-8') as json_file:
        json_file.write(json.dumps(transformed))


if __name__ == "__main__":
    quantity = 5
    start = 100
    total_videos = 250
    r = (total_videos - start) // quantity

    for i in tqdm.tqdm(range(r)):
        try:
            transcribe_playlist("PLzuFY9Ixj9Z6nf7z6t5YmPDTLBgksk8Ts",
                                first_video=start+i*quantity,
                                num_videos=quantity,
                                len_size=200)
        except:
            pass