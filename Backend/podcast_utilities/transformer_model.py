import pandas as pd
import json
from io import StringIO
from sentence_transformers import SentenceTransformer
from constants import MODEL_NAME
from utilities import SingletonMeta

class Model(metaclass=SingletonMeta):
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME, device='cpu')

    # Feeds a pandas dataframe into the transformer
    def feed_dataframe(self, df: pd.DataFrame):
        df["text_vector"] = df["text"].apply(lambda x: self.feed_text(x))
        return df.to_dict("records")

    # Feeds a json style structure into the transformer
    def feed_json(self, js_file: StringIO):
        df = pd.read_json(json.dumps(js_file))
        return self.feed_dataframe(df)

    # Feeds a json string into the transformer
    def feed_json_literal(self, js_str: str):
        json_io = StringIO(js_str)
        return self.feed_json(json_io)

    # Feeds text into the transformer
    def feed_text(self, text):
        return self.model.encode(text)
