import json
import random
from music21 import stream, harmony, midi

# ------------------------------------------------------
# Load trained 2nd-order model
# ------------------------------------------------------

with open("markov_probabilities_2nd_order.json", "r") as f:
    RAW_MODEL = json.load(f)

# Decode "func1|func2" → tuple
PROB_MODEL = {}
for mood, transitions in RAW_MODEL.items():
    PROB_MODEL[mood] = {}
    for key_str, next_probs in transitions.items():
        f1, f2 = key_str.split("|")
        PROB_MODEL[mood][(f1, f2)] = next_probs


# ------------------------------------------------------
# Harmony definitions
# ------------------------------------------------------

FUNCTION_TO_CHORDS = {
    "tonic": ["C", "Am", "Em"],
    "predominant": ["F", "Dm"],
    "dominant": ["G", "Bdim"],
}

FUNCTIONS = {
    "C": "tonic", "Am": "tonic", "Em": "tonic",
    "F": "predominant", "Dm": "predominant",
    "G": "dominant", "Bdim": "dominant",
}

def get_function(ch):
    return FUNCTIONS.get(ch, "tonic")


# ------------------------------------------------------
# Sampling (2nd order + fallback logic)
# ------------------------------------------------------

def sample_next_functions_ranked(mood, func1, func2):
    """
    Return a *sorted list* of (next_function, probability), highest first.
    This is for displaying suggestions to the user.
    """

    if mood not in PROB_MODEL:
        mood = "mixed"

    mood_probs = PROB_MODEL[mood]
    key = (func1, func2)

    # MAIN CASE — exact 2nd-order probabilities
    if key in mood_probs:
        probs = mood_probs[key]
        # sort by probability
        ranked = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        return ranked

    # FALLBACK — merge all first-order transitions (only func2)
    combined = {}

    for (p1, p2), next_probs in mood_probs.items():
        if p2 == func2:
            for f_next, p in next_probs.items():
                combined[f_next] = combined.get(f_next, 0) + p

    if combined:
        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return ranked

    # LAST RESORT
    return [("tonic", 0.33), ("predominant", 0.33), ("dominant", 0.34)]


def choose_chord_from_function(func):
    return random.choice(FUNCTION_TO_CHORDS[func])


# ------------------------------------------------------
# INTERACTIVE SESSION
# ------------------------------------------------------

def interactive_session(start_chord, mood):
    progression = [start_chord]

    print("\nStarting chord:", start_chord)

    # Step 2: choose second chord (function-consistent)
    func1 = get_function(start_chord)
    second_chord = random.choice(FUNCTION_TO_CHORDS[func1])
    progression.append(second_chord)
    print(f"Second chord chosen automatically: {second_chord}")

    while True:
        print("\nCurrent progression:")
        print(" → ".join(progression))

        func_prev2 = get_function(progression[-2])
        func_prev1 = get_function(progression[-1])

        ranked_suggestions = sample_next_functions_ranked(
            mood, func_prev2, func_prev1
        )

        print("\nAI Suggestions (ranked):")
        for i, (func, prob) in enumerate(ranked_suggestions, 1):
            print(f"{i}. {func}  (prob={prob:.3f})")

        user_input = input(
            "\nPick option number OR enter your own chord OR 'done': "
        ).strip()

        if user_input.lower() == "done":
            break

        # Case 1: user selects suggestion by number
        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(ranked_suggestions):
                chosen_func = ranked_suggestions[index][0]
                next_chord = choose_chord_from_function(chosen_func)
                progression.append(next_chord)
                continue
            else:
                print("Invalid number.")
                continue

        # Case 2: user enters chord manually
        if user_input in FUNCTIONS:
            progression.append(user_input)
            continue
        else:
            print("Invalid chord. Try again (C, Am, Em, F, Dm, G, Bdim).")

    return progression


# ------------------------------------------------------
# MIDI
# ------------------------------------------------------

def render_midi(progression, filename="markov_interactive.mid"):
    s = stream.Stream()
    for ch in progression:
        cs = harmony.ChordSymbol(ch)
        cs.quarterLength = 2
        s.append(cs)

    mf = midi.translate.streamToMidiFile(s)
    mf.open(filename, "wb")
    mf.write()
    mf.close()
    print(f"\nMIDI saved as {filename}")


# ------------------------------------------------------
# CLI Entry
# ------------------------------------------------------

if __name__ == "__main__":
    print("\n=== Interactive 2nd-Order Markov Generator ===")

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

    progression = interactive_session(start, mood)

    print("\nFinal progression:")
    print(" → ".join(progression))

    save = input("\nSave MIDI? (y/n): ").lower().startswith("y")
    if save:
        render_midi(progression)
