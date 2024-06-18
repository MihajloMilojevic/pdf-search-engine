from ..trie import Trie, NodeData
from ..graph import PagesGraph
from ..utils import strip_text
from pymupdf import Document
import re

def generate_trie(document: Document):
    trie = Trie()
    for page_number in range(len(document)):
        text: str = document[page_number].get_text("text")
        words_list = strip_text(text).split()
        words = {}
        for i in range(len(words_list)):
            word = words_list[i]
            if word not in words:
                words[word] = (0, [])
            words[word] = (words[word][0] + 1, words[word][1] + [i + 1])
        for word in words:
            trie.insert(word, NodeData(page_number, words[word][1], words[word][0]))
    return trie

def generate_graph(document: Document, page_offset=0):
    graph = PagesGraph(len(document))
    regex = r"see\s*page\s*(\d+)|see\s*pages\s*(\d+)\s*and\s*(\d+)|on\s*page\s*(\d+)"
    for page_number in range(len(document)):
        text: str = document[page_number].get_text("text")
        matches = re.finditer(regex, text, re.IGNORECASE)
        for match in matches:
            for group in match.groups():
                if group is not None:
                    destination_page = int(group) - page_offset
                    if destination_page >= 0 and destination_page < len(document):
                        graph.add_edge(page_number, destination_page)
    return graph