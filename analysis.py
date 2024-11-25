from argparse import ArgumentError
from dataclasses import dataclass
from typing import List, Dict


def count_chars(word_list, index=-1):
    counts = {}
    done = []
    for word in word_list:
        if word in done:
            raise ArgumentError(word, "duplicate")
        if len(word) != 5:
            raise ArgumentError(word, "bad length")
        for i, char in enumerate(word):
            if i == index or index < 0:
                counts[char] = counts.get(char, 0) + 1
        done.append(word)
    return counts

def print_char_map(charcounts):
    for line in [f"{kv[0]}:{kv[1]}" for kv in charcounts]:
        print(line)

def present_char_map(charmap: dict, validate_func = lambda character: True):
    return list(sorted([(key, value) for (key,value) in charmap.items() if validate_func(key)], key=lambda x: x[1], reverse = True))


def analyze(word_list):
    print(f"{len(word_list)} words")
    if word_list:
        print("total")
        print_char_map(present_char_map(count_chars(word_list)))
        for i in range(0,5):
            print(f"character {i + 1}")
            print_char_map(present_char_map(count_chars(word_list, i)))

@dataclass
class WordList:
    words: List[str]

    def __post_init__(self):
        # total in index 0, rest are 1 indexed
        self.indexed_char_counts = [count_chars(self.words, i) for i in range(-1,5)]

    @property
    def total_char_count(self):
        return self.indexed_char_counts[0]

def guess(word, target):
    out = ""
    masked_target = ""
    for i, char in enumerate(target):
        if char != word[i]:
            masked_target += char
        else:
            masked_target += " "
    for i, char in enumerate(word):
        if char != target[i]:
            if char in target:
                if word[:i].count(char) + 1 <= masked_target.count(char):
                    out = out + "y"
                else:
                    out += "b"
            else:
                out += "b"
        else:
            out += "g"
    return out


def solve(the_words):
    guesses = {}
    max_groups = 0
    max_group_keys = []
    for aguess in the_words:
        groups = {}
        for word in the_words:
            if aguess == word:
                continue
            result = guess(aguess, word)
            if result not in groups.keys():
                groups[result] = []
            groups[result].append(word)
        guesses[aguess] = groups
        if len(groups) > max_groups:
            max_groups = len(groups)
            max_group_keys = [aguess]
        elif len(groups) == max_groups:
            max_group_keys.append(aguess)
    return guesses

@dataclass
class GuessResults:
    guess: str
    possibilities:  List[str]

    def __post_init__(self):
        possibility_to_result = {possibility: guess(self.guess, possibility) for possibility in self.possibilities}

        # invert dictionary
        self.results = {result:
                    [possibility for possibility, r in possibility_to_result.items() if r == result]
                for result in possibility_to_result.values()}

    @property
    def groups(self):
        return len(self.results)

    @property
    def largest_group(self):
        return max(len(group) for group in self.results.values())


@dataclass
class GuessGroup:
    guesses: List[str]
    possibilities: List[str]

    def __post_init__(self):
        self.results = {guess: GuessResults(guess, self.possibilities) for guess in self.guesses}

    @property
    def best_groups(self):
        best = []
        best_groups = 0
        for guess, guess_result in self.results.items():
            if guess_result.groups > best_groups:
                best_groups = guess_result.groups
                best = [guess]
            elif guess_result.groups == best_groups:
                best.append(guess)
        return best

    @property
    def best_largest_group(self):
        best = []
        best_largest = 999999999
        for guess, guess_result in self.results.items():
            if guess_result.largest_group < best_largest:
                best_largest = guess_result.largest_group
                best = [guess]
            elif guess_result.groups == best_largest:
                best.append(guess)
        return best



print(guess("theme", "chute"))
words = ["exact", "enact", "caper", "brace", "grace",
         "craze", "crate", "crave", "crane", "chase", "scare", "space"]
analyze(words)
solve(words)

gr = GuessResults(words[0], words)
print(gr.largest_group)

gg = GuessGroup(words, words)