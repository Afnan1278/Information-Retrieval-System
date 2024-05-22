# Contains functions that deal with the extraction of documents from a text file (see PR01)

import json

from document import Document

def extract_collection(source_file_path: str) -> list[Document]:
    """
    Loads a text file (aesopa10.txt) and extracts each of the listed fables/stories from the file.
    :param source_file_name: File name of the file that contains the fables
    :return: List of Document objects
    """
    with open(source_file_path, "r") as json_file:
        lines = json_file.readlines()
    # Ignore lines until "Aesop's Fables"
    while lines:
        if lines.pop(0).strip() == "Aesop's Fables":
            break
    catalog = []
    document_id = 0
    i = 0
    while i < len(lines):
        if lines[i].strip() == "" and i+3 < len(lines) and lines[i+1].strip() == "" and lines[i+2].strip() == "" and lines[i+3].strip() != "":
            i += 3
            title = lines[i].strip()
            i += 3
            raw_text = ""
            while i < len(lines) and lines[i].strip() != "":
                raw_text += lines[i].strip() + " "
                i += 1
            terms = raw_text.split()
            document = Document()
            document.document_id = document_id
            document.title = title
            document.raw_text = raw_text
            document.terms = terms
            catalog.append(document)
            document_id += 1
        else:
            i += 1

    return catalog


def save_collection_as_json(collection: list[Document], file_path: str) -> None:
    """
    Saves the collection to a JSON file.
    :param collection: The collection to store (= a list of Document objects)
    :param file_path: Path of the JSON file
    """

    serializable_collection = []
    for document in collection:
        serializable_collection += [{
            'document_id': document.document_id,
            'title': document.title,
            'raw_text': document.raw_text,
            'terms': document.terms,
            'filtered_terms': document.filtered_terms,
            'stemmed_terms': document.stemmed_terms
        }]

    with open(file_path, "w") as json_file:
        json.dump(serializable_collection, json_file)


def load_collection_from_json(file_path: str) -> list[Document]:
    """
    Loads the collection from a JSON file.
    :param file_path: Path of the JSON file
    :return: list of Document objects
    """
    try:
        with open(file_path, "r") as json_file:
            json_collection = json.load(json_file)

        collection = []
        for doc_dict in json_collection:
            document = Document()
            document.document_id = doc_dict.get('document_id')
            document.title = doc_dict.get('title')
            document.raw_text = doc_dict.get('raw_text')
            document.terms = doc_dict.get('terms')
            document.filtered_terms = doc_dict.get('filtered_terms')
            document.stemmed_terms = doc_dict.get('stemmed_terms')
            collection += [document]

        return collection
    except FileNotFoundError:
        print('No collection was found. Creating empty one.')
        return []
