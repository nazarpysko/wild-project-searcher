from json import JSONEncoder
from typing import TextIO

import pandas as pd
import json
from io import StringIO
from sentence_transformers import SentenceTransformer
from constants import MODEL_NAME
from utilities import SingletonMeta
import os
import numpy as np


class Model(metaclass=SingletonMeta):
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    # Feeds a pandas dataframe into the transformer
    def feed_dataframe(self, df: pd.DataFrame):
        df["text_vector"] = df["text"].apply(lambda x: self.feed_text(x))
        return df.to_dict("records")

    # Feeds a json string into the transformer
    def feed_json_literal(self, js_str: str):
        json_io = StringIO(js_str)
        df = pd.read_json(json_io)
        return self.feed_dataframe(df)

    # Feeds a json style structure into the transformer
    def feed_json(self, js_file: TextIO):
        js = json.load(js_file)
        return self.feed_json_literal(js)

    # Feeds text into the transformer
    def feed_text(self, text):
        return self.model.encode(text)


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


if __name__ == "__main__":
    model = Model()

    read_path = "../documents/initial/normal"
    save_path = "../documents/initial/modeled"

    files = os.listdir(read_path)

    for file_name in files:
        file_read_path = read_path + "/" + file_name
        file_save_path_trs = save_path + "/" + file_name.split('.')[0] + "_trs.json"
        file_save_path_text = save_path + "/" + file_name.split('.')[0] + "_text.json"

        with open(file_read_path, "r", encoding='utf-8') as file:
            print("loading:", file_name)

            transcriptions, full_text = json.load(file)
            js_trs = json.dumps(transcriptions)
            js_text = json.dumps(full_text)

            modeled_trs = model.feed_json_literal(js_trs)
            modeled_text = model.feed_json_literal(js_text)

            open_type = "x"
            if os.path.exists(file_save_path_trs):
                open_type = "w"

            with open(file_save_path_trs, open_type, encoding='utf-8') as file2:
                file2.write(json.dumps(modeled_trs, cls=NumpyArrayEncoder))

            with open(file_save_path_text, open_type, encoding='utf-8') as file2:
                file2.write(json.dumps(modeled_text, cls=NumpyArrayEncoder))