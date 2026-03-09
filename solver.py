from collections import Counter

with open("/Users/ece/Desktop/wordle-solver/words.txt") as f:
    all_words = [w.strip().lower() for w in f if len(w.strip()) == 5]

def matches(word, guess, result):
    for i, (g, r) in enumerate(zip(guess, result)):
        if r == 'G':
            if word[i] != g:
                return False
        elif r == 'Y':
            if g not in word:
                return False
            if word[i] == g:
                return False
        elif r == 'X':
            if g in word:
                return False
    return True

def filter_words(words, guess, result):
    return [word for word in words if matches(word, guess, result)]

def best_guess(words):
    freq = Counter()
    for word in words:
        for letter in set(word):
            freq[letter] += 1
    def score(word):
        return sum(freq[letter] for letter in set(word))
    return max(words, key=score)

words = all_words.copy()

while True:
    suggestion = best_guess(words)
    print(f"\nSuggestion: {suggestion}")
    print(f"Remaining words: {len(words)}")
    
    guess = input("Your guess: ").strip().lower()
    result = input("Result (G/Y/X): ").strip().upper()
    
    if result == "GGGGG":
        print("Solved!")
        break
    
    words = filter_words(words, guess, result)
    
    if len(words) == 0:
        print("No words left, something went wrong.")
        break