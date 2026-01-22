import json
import random

# ------------------------------------------------------
# Functional Harmony Knowledge
# ------------------------------------------------------

FUNCTIONS = {
    "C": "tonic", "Am": "tonic", "Em": "tonic",
    "F": "predominant", "Dm": "predominant",
    "G": "dominant", "Bdim": "dominant",
}

MOOD_BY_FUNCTION = {
    "tonic": "stable / floating",
    "predominant": "gentle motion",
    "dominant": "tension / drive",
}

RESOLUTION_MAP = {
    "dominant": ["tonic"],
    "predominant": ["dominant"],
    "tonic": ["predominant", "dominant"]
}

KEY_CHORDS = ["C", "Dm", "Em", "F", "G", "Am", "Bdim"]

MOODS = [
    "stable / floating",
    "gentle motion",
    "tension / drive",
    "mixed"
]

# ------------------------------------------------------
# Helpers
# ------------------------------------------------------

def get_function(ch):
    return FUNCTIONS.get(ch, "tonic")

def get_mood(ch):
    return MOOD_BY_FUNCTION[get_function(ch)]

def suggest_next(prev_chord, mood_filter):
    prev_func = get_function(prev_chord)
    target_funcs = RESOLUTION_MAP.get(prev_func, ["tonic"])

    candidates = []
    for ch in KEY_CHORDS:
        if get_function(ch) in target_funcs:
            mood = get_mood(ch)
            if mood_filter != "mixed" and mood != mood_filter:
                continue
            candidates.append(ch)

    # fallback if mood too strict
    if not candidates:
        for ch in KEY_CHORDS:
            if get_function(ch) in target_funcs:
                candidates.append(ch)

    return candidates

# ------------------------------------------------------
# Dataset generation
# ------------------------------------------------------

def generate_dataset(
    num_sessions=500,
    max_length=8,
    output_file="chords_dataset.json"
):
    dataset = []

    for _ in range(num_sessions):
        mood = random.choice(MOODS)
        progression = [random.choice(KEY_CHORDS)]

        for step in range(1, max_length):
            prev = progression[-1]
            suggestions = suggest_next(prev, mood)

            if not suggestions:
                break

            next_chord = random.choice(suggestions)

            # Store clean AI training sample
            example = {
                "context": progression.copy(),
                "functions": [get_function(ch) for ch in progression],
                "mood": mood,
                "next_chord": next_chord
            }
            dataset.append(example)

            progression.append(next_chord)

    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"Dataset created: {len(dataset)} samples")
    print(f"Saved as: {output_file}")

# ------------------------------------------------------
# RUN
# ------------------------------------------------------

if __name__ == "__main__":
    generate_dataset(num_sessions=10000, max_length=8)
