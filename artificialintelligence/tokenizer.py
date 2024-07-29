import json



#this class will be used instead of the keras tokenizer, it will tokenize, pad, convert to sequences and convert back to data
class TokenEngine:
    def __init__(self,oov_token="<OOV>",char_level=False,lower=True,filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'):
        self.oov_token = oov_token
        self.char_level = char_level
        self.lower = lower
        self.filters = filters
        self.vocab = {}
        self.vocab[self.oov_token] = 1


    def dictionary(self):
        #return all the properties of this class
        return {"oov_token":self.oov_token,"char_level":self.char_level,"lower":self.lower,"filters":self.filters,"vocab":self.vocab}

    def to_json(self):
        #save all the properties of this class to a json file
        return json.dumps(self.dictionary(),indent=4)
    def from_json(self,text):
        #load all the properties of this class from a json file
        json_data = dict(json.loads(text))
        self.oov_token = json_data["oov_token"]
        self.char_level = json_data["char_level"]
        self.lower = json_data["lower"]
        self.filters = json_data["filters"]
        self.vocab = json_data["vocab"]

    def filter_the_word(self,word : str ):
        for filter_char in self.filters:
            word = word.replace(filter_char,"")
        #remove spaces from the word
        word = word.replace(" ","")
        return word
    def is_this_word_in_vocab(self,word):
        try:
            index = self.vocab[word]
            return True
        except:
            return False
    def add_word_to_vocab(self,word):
        iterator = len(self.vocab)
        self.vocab[word] = iterator+1

    def word_index(self,word):
        #return the index of the word
        index = 1
        if self.is_this_word_in_vocab(word):
            index = self.vocab[word]
        return index
    def index_word(self,index):
        #return the word of the index
        for key,value in self.vocab.items():
            if value == index:
                return key
        return self.oov_token

    def get_words_from_sentence(self,sentence : str):
        wordlist : list = []
        split_sentence = sentence.split(" ")
        for word in split_sentence:
            if word != " ":
                wordlist.append(word)
        return wordlist
    def fit_on_texts(self,data : list):
        #fit the vocab on the data, if the word is not in the vocab, add it if it is, do nothing. apply filters, oov_token, char_level and lower
        for sentence in data:
            words = self.get_words_from_sentence(sentence)
            for word in words:
                inspectedword = self.filter_the_word(word)
                if self.lower:
                    inspectedword = inspectedword.lower()
                if not self.is_this_word_in_vocab(inspectedword):
                    self.add_word_to_vocab(inspectedword)




    def texts_to_sequences(self,data):
        #convert the data to sequences, if the word is not in the vocab, replace it with the oov_token
        sequences = []
        for sentence in data:
            sequence = []
            words = self.get_words_from_sentence(sentence)
            for word in words:
                inspectedword = self.filter_the_word(word)
                if self.lower:
                    inspectedword = inspectedword.lower()
                #(inspectedword)
                sequence.append(self.word_index(inspectedword))
            sequences.append(sequence)
        return sequences
    def sequences_to_texts(self,sequences):
        #convert the sequences back to data
        data = []
        for sequence in sequences:
            words = []
            for index in sequence:

                words.append(self.index_word(index))
            data.append(" ".join(words))
        return data

    def pad_sequences(self, sequences, maxlen=10000, padding="post", truncating="post"):
        # pad the sequences
        for sequence in sequences:
            print(sequence)
            if maxlen < len(sequence):
                sequence = sequence[:maxlen]
            amount_of_padding = maxlen - len(sequence)
            if padding == "post":
                for i in range(amount_of_padding):
                    sequence.append(0)
            elif padding == "pre":
                for i in range(amount_of_padding):
                    sequence.insert(0, 0)

        return sequences

    def remove_padding(self,sequence : list):
#remove the padding from the sequence
        while sequence[0] == 0:
            sequence.pop(0)
        while sequence[-1] == 0:
            sequence.pop()
        return sequence






class Tokenizer:
    def __init__(self, path=None):
        if path is None:
            self.tokenizer = TokenEngine(oov_token="<OOV>",
                                         char_level=False,
                                         lower=True)
        else:
            self.load_vocab(path)

    def fit_on_texts_from_path(self, path):
        with open(path, "r") as file:
            new_data = json.load(file)
            self.tokenizer.fit_on_texts(new_data)

    def fit_on_texts(self, data: list):
        self.tokenizer.fit_on_texts(data)

    def save_vocab(self, path):
        text = self.tokenizer.to_json()
        with open(path, "w") as file:
            file.write(text)

    def load_vocab(self, path):
        with open(path, "r") as file:
            text = file.read()
        self.tokenizer = TokenEngine()
        self.tokenizer.from_json(text)
        # self.tokenizer.char_level = False

    def pad_sequences(self, sequences, maxlen=10000, padding="post", truncating="post"):
        #return keras.preprocessing.sequence.pad_sequences(sequences, maxlen=maxlen, padding=padding,
         #                                                 truncating=truncating)
        self.tokenizer.pad_sequences(sequences, maxlen=maxlen, padding=padding, truncating=truncating)
    def data_to_sequences(self, data : list ):
        return self.tokenizer.texts_to_sequences(data)

    def sequences_to_data(self, sequences : list ):
        return self.tokenizer.sequences_to_texts(sequences)

    def data_to_padded_sequences(self, data, maxlen=10000, padding="post", truncating="post"):
        return self.pad_sequences(self.data_to_sequences(data), maxlen=maxlen, padding=padding, truncating=truncating)
    def apply_basic_grammar(self,sentence : str):
        import re
        # Capitalize the first letter of the sentence
        sentence = sentence.capitalize()

        # Use regular expressions to correctly capitalize "I" in contractions
        corrected_sentence = re.sub(r'\bi(?=[\'’]m|\b|\'m|\'ve|\'d|\'ll)\b', 'I', sentence, flags=re.IGNORECASE)

        return corrected_sentence


