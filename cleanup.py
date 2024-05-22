# Contains all functions that deal with stop word removal.
import json
import os
import string
from collections import Counter
from document import Document
try:
    DATA_PATH = 'data'
    STOPWORD_FILE_PATH = os.path.join(DATA_PATH, 'stopwords.json')
    with open(STOPWORD_FILE_PATH, 'r') as f:
        stop_word_list = json.load(f)
except FileNotFoundError:
            print('No stopword list was found.')
            stop_word_list = []

def remove_symbols(text_string: str) -> str:
    """
    Removes all punctuation marks and similar symbols from a given string.
    Occurrences of "'s" are removed as well.
    :param text:
    :return:
    """

    text_string = text_string.replace("'s", "")
    text_string = text_string.translate(str.maketrans('', '', string.punctuation))
    return text_string


def is_stop_word(term: str) -> bool:
    
    """
    Checks if a given term is a stop word.
    :param stop_word_list: List of all considered stop words.
    :param term: The term to be checked.
    :return: True if the term is a stop word.
    """
    return term in stop_word_list


def remove_stop_words_from_term_list(term_list: list[str]) -> list[str]:
    """
    Takes a list of terms and removes all terms that are stop words.
    :param term_list: List that contains the terms
    :return: List of terms without stop words
    """
    # Hint:  Implement the functions remove_symbols() and is_stop_word() first and use them here.
    return [term for term in term_list if not is_stop_word(term)]


def filter_collection(collection: list[Document]):
    """
    For each document in the given collection, this method takes the term list and filters out the stop words.
    Warning: The result is NOT saved in the documents term list, but in an extra field called filtered_terms.
    :param collection: Document collection to process
    """
    # Hint:  Implement remove_stop_words_from_term_list first and use it here.
    for document in collection:
        document.filtered_terms = remove_stop_words_from_term_list(document.terms)


def load_stop_word_list(raw_file_path: str) -> list[str]:
    """
    Loads a text file that contains stop words and saves it as a list. The text file is expected to be formatted so that
    each stop word is in a new line, e. g. like englishST.txt
    :param raw_file_path: Path to the text file that contains the stop words
    :return: List of stop words
    """
    with open(raw_file_path, 'r') as f:
        stop_word_list = f.read().splitlines()
    return stop_word_list

def create_stop_word_list_by_frequency(collection: list[Document]) -> list[str]:
    """
    Uses the method of J. C. Crouch (1990) to generate a stop word list by finding high and low frequency terms in the
    provided collection.
    :param collection: Collection to process
    :return: List of stop words
    """
    all_terms = []
    for document in collection:
        for term in document.terms:
            all_terms.append(term)
    
    term_frequency = Counter(all_terms)
    
    # Sort the terms by frequency in descending order
    sorted_terms = sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)
    
    # Determine the high and low frequency terms. high frequency terms are the 10% most frequent terms, low frequency terms are the 10% least frequent terms
    num_terms = len(sorted_terms)
    high_frequency_terms = [term for term, freq in sorted_terms[:num_terms//10]]
    low_frequency_terms = [term for term, freq in sorted_terms[-num_terms//10:]]
    
    # Combine the high and low frequency terms to create the stop word list
    stop_word_list = high_frequency_terms + low_frequency_terms
    
    return stop_word_list
    