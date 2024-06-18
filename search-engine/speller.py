from spellchecker import SpellChecker

def suggest_corrections(word):
    spell = SpellChecker()
    # Find the most probable correction
    correction = spell.correction(word)
    # Find a list of suggestions
    suggestions = spell.candidates(word)
    return correction, suggestions


if __name__ == '__main__':
    d = {"a": 1, "b": 2, "c": 3}
    while True:
        word = input("Enter a word: ")
        if word == "exit":
            break
        correction, suggestions = suggest_corrections(word)
        print(f"Correction: {correction}")
        print(f"Suggestions: {suggestions}")
