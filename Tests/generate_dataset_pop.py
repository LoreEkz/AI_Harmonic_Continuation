import json
import random

# ===============================
# User Settings
# ===============================
NUM_PROGRESSIONS = 10000  # How many progressions to generate
MIN_LENGTH = 3             # Min chords in a progression
MAX_LENGTH = 6             # Max chords in a progression
INCLUDE_EXTENSIONS = True  # Add 7th/9th/13th to some chords

# ===============================
# Chords and Functional Roles
# ===============================
CHORDS = {
    "T": ["C", "Am", "Em"],
    "PD": ["F", "Dm"],
    "D": ["G", "E"]
}

EXTENSIONS = ["7", "maj7", "9", "13"]

# Probability of adding an extension
EXT_PROB = 0.3

# ===============================
# Helper Functions
# ===============================
def add_extension(chord):
    if INCLUDE_EXTENSIONS and random.random() < EXT_PROB:
        ext = random.choice(EXTENSIONS)
        return chord + ext
    return chord

def get_next_chord(prev_func):
    """Choose next chord based on functional progression rules"""
    if prev_func == "T":
        # T -> PD or D
        func = random.choices(["PD", "D", "T"], [0.5, 0.3, 0.2])[0]
    elif prev_func == "PD":
        # PD -> D or T
        func = random.choices(["D", "T", "PD"], [0.5, 0.3, 0.2])[0]
    elif prev_func == "D":
        # D -> T or PD
        func = random.choices(["T", "PD", "D"], [0.6, 0.3, 0.1])[0]
    else:
        func = "T"
    chord = random.choice(CHORDS[func])
    chord = add_extension(chord)
    return chord, func

# ===============================
# Generate Dataset
# ===============================
dataset = []

for _ in range(NUM_PROGRESSIONS):
    length = random.randint(MIN_LENGTH, MAX_LENGTH)
    progression = []

    # Start with a tonic
    chord = add_extension(random.choice(CHORDS["T"]))
    func = "T"
    progression.append({"current_chord": chord, "function": func})

    for _ in range(length - 1):
        chord, func = get_next_chord(func)
        progression.append({"current_chord": chord, "function": func})

    # Add chosen_next_chord for multi-step context
    for i in range(len(progression) - 1):
        progression[i]["chosen_next_chord"] = progression[i + 1]["current_chord"]

    dataset.append(progression)

# Save to dataset.json
with open("dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"Dataset generated with {NUM_PROGRESSIONS} progressions, saved to dataset.json")
