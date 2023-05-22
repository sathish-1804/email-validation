from popular_domains import emailDomains
import jellyfish
from typing import List
from concurrent.futures import ThreadPoolExecutor
import numpy as np

class TrieNode:
    def __init__(self, char: str):
        self.char = char
        self.children = {}
        self.word_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode('')

    def add(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        node.word_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.word_end

def suggest_email_domain(domain: str, valid_domains: List[str]) -> List[str]:
    # Build a trie with valid domains
    trie = Trie()
    for valid_domain in valid_domains:
        trie.add(valid_domain)

    # Calculate distances using a faster string distance metric
    distances = {}
    with ThreadPoolExecutor(max_workers=np.minimum(16, len(valid_domains))) as executor:
        for valid_domain, distance in zip(valid_domains, executor.map(lambda x: jellyfish.damerau_levenshtein_distance(domain, x), valid_domains)):
            if distance <= 2:
                if distance in distances:
                    if valid_domain not in distances[distance]:
                        distances[distance].append(valid_domain)
                else:
                    distances[distance] = [valid_domain]

    # Choose the most similar domains based on alphabetical order
    sorted_domains = np.array([])
    if distances:
        min_distance = min(distances.keys())
        sorted_domains = sorted(distances[min_distance])
        sorted_domains = [d for d in sorted_domains if trie.search(d)]

    # Check for phonetic similarity using Soundex
    soundex_domain = jellyfish.soundex(domain)
    phonetically_similar_domains = [d for d in valid_domains if jellyfish.soundex(d) == soundex_domain and d not in sorted_domains]

    # Combine and return the results
    return sorted_domains + phonetically_similar_domains


# # Example usage
# domain = "yaho.c.m"
# suggested_domain = suggest_email_domain(domain, emailDomains)
# print(suggested_domain)
