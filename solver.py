from collections import Counter
import math
from tqdm import tqdm

with open("/Users/ece/Desktop/wordle-solver/words.txt") as f:
    all_words = [w.strip().lower() for w in f if len(w.strip()) == 5]

def get_pattern(guess, answer):
    pattern = ['X'] * 5
    answer_chars = list(answer)
    
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = 'G'
            answer_chars[i] = None
    
    for i in range(5):
        if pattern[i] == 'G':
            continue
        if guess[i] in answer_chars:
            pattern[i] = 'Y'
            answer_chars[answer_chars.index(guess[i])] = None
    
    return ''.join(pattern)

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
    best_word = None
    best_entropy = -1
    
    for guess in tqdm(words, desc="Calculating"):
        pattern_counts = Counter()
        for answer in words:
            pattern = get_pattern(guess, answer)
            pattern_counts[pattern] += 1
        
        entropy = 0
        total = len(words)
        for count in pattern_counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        
        if entropy > best_entropy:
            best_entropy = entropy
            best_word = guess
    
    return best_word

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