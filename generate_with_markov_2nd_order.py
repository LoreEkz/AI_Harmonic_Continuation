import json
import random
from music21 import stream, harmony, midi

# ------------------------------------------------------
# Load trained 2nd-order Markov model
# ------------------------------------------------------

with open("markov_probabilities_2nd_order.json", "r") as f:
    RAW_MODEL = json.load(f)

# Decode "func1|func2" → (func1, func2)
PROB_MODEL = {}

for mood, transitions in RAW_MODEL.items():
    PROB_MODEL[mood] = {}
    for key_str, next_probs in transitions.items():
        func1, func2 = key_str.split("|")
        PROB_MODEL[mood][(func1, func2)] = next_probs


# ------------------------------------------------------
# Basic harmony setup
# ------------------------------------------------------

FUNCTION_TO_CHORDS = {
    "tonic": ["C", "Am", "Em"],
    "predominant": ["F", "Dm"],
    "dominant": ["G", "Bdim"]
}

FUNCTIONS = {
    "C": "tonic", "Am": "tonic", "Em": "tonic",
    "F": "predominant", "Dm": "predominant",
    "G": "dominant", "Bdim": "dominant",
}

def get_function(ch):
    return FUNCTIONS.get(ch, "tonic")


# ------------------------------------------------------
# Sampling logic
# ------------------------------------------------------

def sample_next_function(mood, func1, func2):
    """
    Sample next harmonic function using 2nd-order Markov probabilities.
    Includes fallback to 1st-order, then random if needed.
    """

    # Fallback mood if not found
    if mood not in PROB_MODEL:
        mood = "mixed"

    mood_probs = PROB_MODEL[mood]
    key = (func1, func2)

    # CASE 1 — Exact 2nd-order match
    if key in mood_probs:
        probs = mood_probs[key]
        funcs = list(probs.keys())
        weights = list(probs.values())
        return random.choices(funcs, weights=weights)[0]

    # CASE 2 — Fallback: 1st-order (match only func2)
    combined = {}

    for (p1, p2), next_probs in mood_probs.items():
        if p2 == func2:  # match last function
            for next_func, prob in next_probs.items():
                combined[next_func] = combined.get(next_func, 0) + prob

    if combined:
        funcs = list(combined.keys())
        weights = list(combined.values())
        return random.choices(funcs, weights=weights)[0]

    # CASE 3 — Total fallback: random choice
    return random.choice(["tonic", "predominant", "dominant"])


def choose_chord_from_function(func):
    """Pick a chord belonging to a harmonic function."""
    return random.choice(FUNCTION_TO_CHORDS[func])


# ------------------------------------------------------
# Generate full progression
# ------------------------------------------------------

def generate_progression(start_chord, mood="mixed", length=8):
    """
    Build harmonic progression using 2nd-order Markov chain.
    """
    progression = [start_chord]

    # If progression is only one chord long
    if length < 2:
        return progression

    # Generate second chord from same function
    func1 = get_function(start_chord)
    second_chord = random.choice(FUNCTION_TO_CHORDS[func1])
    progression.append(second_chord)

    # Now continue with 2nd-order logic
    for _ in range(length - 2):
        f_prev2 = get_function(progression[-2])
        f_prev1 = get_function(progression[-1])

        next_func = sample_next_function(mood, f_prev2, f_prev1)
        next_chord = choose_chord_from_function(next_func)

        progression.append(next_chord)

    return progression


# ------------------------------------------------------
# MIDI export
# ------------------------------------------------------

def render_midi(progression, filename="markov_2nd_order.mid"):
    s = stream.Stream()
    for ch in progression:
        cs = harmony.ChordSymbol(ch)
        cs.quarterLength = 2
        s.append(cs)

    mf = midi.translate.streamToMidiFile(s)
    mf.open(filename, "wb")
    mf.write()
    mf.close()
    print(f"MIDI saved as {filename}")


# ------------------------------------------------------
# CLI Interface
# ------------------------------------------------------

if __name__ == "__main__":
    print("\n=== 2nd-Order Markov Progression Generator ===")

    start = input("Enter starting chord (C, Am, F, etc.): ").strip()
    if start not in FUNCTIONS:
        print("Invalid chord. Using C.")
        start = "C"

    print("\nSelect mood:")
    print("1. tension / drive")
    print("2. stable / floating")
    print("3. gentle motion")
    print("4. mixed")

    mood_map = {
        "1": "tension / drive",
        "2": "stable / floating",
        "3": "gentle motion",
        "4": "mixed"
    }

    mood = mood_map.get(input("> "), "mixed")

    length = input("\nProgression length (default 8): ").strip()
    length = int(length) if length.isdigit() else 8

    progression = generate_progression(start, mood, length)

    print("\nGenerated progression:")
    print(" → ".join(progression))

    save = input("\nSave MIDI? (y/n): ").lower().startswith("y")
    if save:
        render_midi(progression)

