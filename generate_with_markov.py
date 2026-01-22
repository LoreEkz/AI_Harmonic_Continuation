import json
import random
from music21 import stream, harmony, midi

# ------------------------------------------------------
# LOAD TRAINED MARKOV MODEL
# ------------------------------------------------------

with open("markov_probabilities.json", "r") as f:
    PROB_MODEL = json.load(f)

# ------------------------------------------------------
# BASIC HARMONY SETUP
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
# PROBABILITY SAMPLING
# ------------------------------------------------------

def sample_next_function(mood, current_function):
    """Choose next function using trained Markov probabilities."""
    if mood not in PROB_MODEL:
        mood = "mixed"

    mood_probs = PROB_MODEL[mood]

    if current_function not in mood_probs:
        return random.choice(["tonic", "predominant", "dominant"])

    prob_dict = mood_probs[current_function]
    funcs = list(prob_dict.keys())
    weights = list(prob_dict.values())

    return random.choices(funcs, weights=weights)[0]

def choose_chord_from_function(func):
    """Pick a chord belonging to a harmonic function."""
    return random.choice(FUNCTION_TO_CHORDS[func])

# ------------------------------------------------------
# GENERATE PROGRESSION
# ------------------------------------------------------

def generate_progression(start_chord, mood="mixed", length=8):
    progression = [start_chord]
    current = start_chord

    for _ in range(length - 1):
        curr_function = get_function(current)
        next_function = sample_next_function(mood, curr_function)
        next_chord = choose_chord_from_function(next_function)

        progression.append(next_chord)
        current = next_chord

    return progression

# ------------------------------------------------------
# MIDI RENDERING
# ------------------------------------------------------

def render_midi(progression, filename="markov_progression.mid"):
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
# USER MODE
# ------------------------------------------------------

if __name__ == "__main__":
    print("\n=== Markov Progression Generator (No Extensions) ===")

    start = input("Enter starting chord (C, Am, F, etc.): ").strip()
    if start not in FUNCTIONS:
        print("Invalid chord -> using C.")
        start = "C"

    print("\nSelect mood conditioning:")
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

    length = input("\nHow many chords? (default 8): ").strip()
    length = int(length) if length.isdigit() else 8

    progression = generate_progression(start, mood, length)

    print("\nGenerated progression:")
    print(" → ".join(progression))

    save = input("\nSave MIDI? (y/n): ").lower().startswith("y")
    if save:
        render_midi(progression)
