from gensim import corpora, models
from iter_class import IterDocs, MyCorpus
from tfidf import low_tfidf_terms
import os


def load_serialize(input_path, output_path):
    """
    serialize original corpus, dict and tfidf model
    """

    text_iter = IterDocs(input_path)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(line for line in text_iter)
    dictionary.filter_extremes(no_below=3, no_above=0.95)
    dictionary.compactify()
    dictionary.save(os.path.join(output_path, "dictionary"))

    # convert tokenized documents into a document-term matrix
    corpus = MyCorpus(input_path, dictionary)
    tfidf = models.TfidfModel(corpus)
    # use tfidf-lized corpus instead of original one
    corpora.MmCorpus.serialize(os.path.join(output_path, 'SerializedCorpus.mm'), tfidf[corpus])

    # initialize a tfidf transformation
    tfidf.save(os.path.join(output_path, "tfidf_model"))


def filter_tfidf(input_path, output_path, threshold=0.05):
    low_value_words = low_tfidf_terms(output_path, threshold)
    dictionary = corpora.Dictionary.load(os.path.join(output_path, "dictionary"))

    dictionary.filter_tokens(low_value_words)
    dictionary.filter_extremes()
    dictionary.compactify()
    dictionary.save(os.path.join(output_path, "new_dictionary"))
    new_corpus = MyCorpus(input_path, dictionary)
    corpora.MmCorpus.serialize(os.path.join(output_path, 'new_SerializedCorpus.mm'), new_corpus)


