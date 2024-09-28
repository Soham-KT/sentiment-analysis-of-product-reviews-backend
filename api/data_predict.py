import dill as pk
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from data_loader import ModelLoader, TokenizerLoader
import re
from nltk.corpus import stopwords


TAG_RE = re.compile(r'<[^>]+>')

MODEL_LOADER = ModelLoader.get_instance()
lstm_model = MODEL_LOADER.get_data()

TOKENIZER_LOADER = TokenizerLoader.get_instance()
lstm_tokenizer = TOKENIZER_LOADER.get_data()

def remove_tags(text):
    return TAG_RE.sub('', text)


def preprocess_text(text):
    # remove tags and convert to lowercase
    sentence = remove_tags(text).lower()

    # remove punctuation, numbers, and single characters, and collapse multiple spaces
    sentence = re.sub(r'[^a-z\s]', ' ', sentence)  # remove non-alphabetic characters
    sentence = re.sub(r'\b[a-z]\b', '', sentence)  # remove single characters
    sentence = re.sub(r'\s+', ' ', sentence).strip()  # collapse multiple spaces

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    sentence = ' '.join([word for word in sentence.split() if word not in stop_words])
    
    return sentence


def model_predict(text, tokenizer=lstm_tokenizer, model=lstm_model):
    clean_text = preprocess_text(text)
    sequence = tokenizer.texts_to_sequences([clean_text])
    padded_sequence = pad_sequences(sequence, maxlen=100)
    prediction = model.predict(padded_sequence)
    prediction = 'Negative' if prediction< 0.5 else 'Positive'
    
    return prediction


if __name__ == '__main__':
    text = "This DVD will be a disappointment if you get it hoping to see some substantial portion of the acts of the various comics listed on the cover. All you get here are snippets of performance, at best. The rest is just loose-leaf reminiscence about the good old days in Boston, in the early 80's, when a lot of comics were hanging out together and getting their start.It's like a frat house reunion. There's a lot of lame nostalgia. There are quite a few guffaws recalling jokes (practical and otherwise)perpetrated - back then. But you had to have been there to appreciate all the basically good ol' boy camaraderie. If you weren't actually a part of that scene, all this joshing and jostling will fall flat.If you want to actually hear some of these comics' routines - you will have to look elsewhere."
    
    print(model_predict(text))