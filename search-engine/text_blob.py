from textblob import TextBlob

def suggest_corrections(word):
    blob = TextBlob(word)
    # Get the corrected word
    correction = blob.correct()
    # TextBlob doesn't provide multiple suggestions directly
    suggestions = [correction]
    return correction, suggestions


if __name__ == '__main__':
    while True:
        word = input("Enter a word: ")
        if word == "exit":
            break
        correction, suggestions = suggest_corrections(word)
        print(f"Correction: {correction}")
        print(f"Suggestions: {suggestions}")
