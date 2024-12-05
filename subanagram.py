import sys
from itertools import permutations, combinations


def load_words(filename):
    with open(filename) as f:
        return set(word.strip().lower() for word in f)


def subanagrams(word, word_list):
    subanagrams = set()
    for i in range(1, len(word) + 1):
        for subset in combinations(word, i):
            for perm in permutations(subset):
                subanagram = ''.join(perm)
                if subanagram in word_list:
                    subanagrams.add(subanagram)
    for perm in permutations(word):
        anagram = ''.join(perm)
        if anagram in word_list:
            subanagrams.add(anagram)
    return subanagrams


def main():
    if len(sys.argv) < 3:
        print("Usage: python subanagrams.py word_list_file word1 [word2 ...]")
        sys.exit(1)

    word_list_file = sys.argv[1]
    words = sys.argv[2:]

    word_list = load_words(word_list_file)

    subanagrams_set = set()
    for word in words:
        subanagrams_set.update(subanagrams(word, word_list))
    subanagrams_list = sorted(list(subanagrams_set))
    print(f"Subanagrams and anagrams: {', '.join(subanagrams_list)}")


if __name__ == '__main__':
    main()
