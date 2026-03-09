# Wordle Solver 🟩🟨⬛

A Python-based Wordle solver that suggests the best next guess using letter frequency analysis, built as a learning project with AI-assisted development using Claude.

---

## How It Works

The solver reads a list of ~2300 five-letter words (sourced from NYT's Wordle word list) and narrows down candidates after each guess using the colored feedback Wordle gives you.

### The feedback system

After each guess, Wordle gives you three types of clues:

| Color | Code | Meaning |
|-------|------|---------|
| 🟩 Green | `G` | Correct letter, correct position |
| 🟨 Yellow | `Y` | Correct letter, wrong position |
| ⬛ Gray | `X` | Letter not in the word |

### Core logic

**1. `matches(word, guess, result)`**  
The heart of the solver. For every word in our list, this function checks whether it's still a valid candidate given the feedback we received.

```python
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
```

**2. `filter_words(words, guess, result)`**  
Filters the full word list down to only valid candidates after each guess.

**3. `best_guess(words)`**  
Picks the best next guess by scoring each word based on letter frequency. The idea: a word that contains letters appearing in many remaining candidates gives us the most information.

```python
def best_guess(words):
    freq = Counter()
    for word in words:
        for letter in set(word):
            freq[letter] += 1
    def score(word):
        return sum(freq[letter] for letter in set(word))
    return max(words, key=score)
```

---

## Usage

```bash
python solver.py
```

The solver suggests a word. You type that word into Wordle, then enter the result:

```
Suggestion: crane
Remaining words: 2309

Your guess: crane
Result (G/Y/X): XXYXX

Suggestion: foist
Remaining words: 312
...
```

Repeat until `GGGGG` - solved!

---

## Why Not Entropy?

I also explored an entropy-based approach (available in the [`entropy-approach`](https://github.com/eceylcn/wordle-solver/tree/entropy-approach) branch). Instead of letter frequency, it calculates how much information each guess provides on average using Shannon entropy:

```
H(guess) = -Σ p(pattern) * log₂(p(pattern))
```

For each candidate guess, it simulates all possible G/Y/X outcomes and finds the word that splits the remaining list most evenly - maximizing information gain.

**So why didn't I use it?**  
On a ~2300 word list, the practical difference in solving speed (number of guesses) is minimal. But the computational cost is significant: the entropy version runs O(n²) pattern comparisons on every turn, making it noticeably slower. For this scale, letter frequency is fast, simple, and performs just as well.

Entropy would shine on a much larger word list or if we pre-computed the first guess offline and cached it.

---

## What I Learned

- How to model constraint satisfaction problems in Python
- Why data structure choices matter - the word list source makes a huge difference in result quality
- The trade-off between algorithmic sophistication and practical performance
- Git branching as a way to experiment without breaking working code
- That "smarter" doesn't always mean "better" for the problem at hand

---

## Setup

```bash
# Get the word list
curl -o words.txt https://raw.githubusercontent.com/tabatkins/wordle-list/main/words

# Run
python solver.py
```

Requires Python 3.x, no external dependencies for the main version.

---

## Branch Structure

| Branch | Description |
|--------|-------------|
| `main` | Letter frequency approach - fast and practical |
| `entropy-approach` | Shannon entropy approach - smarter algorithm, slower runtime |
