import json
from collections import defaultdict

# ===================================================
# STEP 1 — Load dataset
# ===================================================

with open("chord_dataset.json", "r") as f:
    data = json.load(f)

# ===================================================
# STEP 2 — Train Markov model (count transitions)
# ===================================================

# model[mood][current_function][next_function] = count
model = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

FUNCTIONS = {
    "C": "tonic", "Am": "tonic", "Em": "tonic",
    "F": "predominant", "Dm": "predominant",
    "G": "dominant", "Bdim": "dominant",
}

def get_function(ch):
    return FUNCTIONS.get(ch, "tonic")

print("Counting transitions...")

for sample in data:
    mood = sample["mood"]
    functions = sample["functions"]
    next_chord = sample["next_chord"]

    current_function = functions[-1]
    next_function = get_function(next_chord)

    model[mood][current_function][next_function] += 1

print("Training complete — raw counts collected.")

# ===================================================
# STEP 3 — Convert counts → probabilities (normalization)
# ===================================================

prob_model = defaultdict(dict)

print("Normalizing counts into probabilities...")

for mood in model:
    prob_model[mood] = {}
    for curr_func in model[mood]:

        total = sum(model[mood][curr_func].values())

        prob_model[mood][curr_func] = {}

        for next_func, count in model[mood][curr_func].items():
            prob_model[mood][curr_func][next_func] = count / total

print("Normalization complete.")

# ===================================================
# STEP 4 — Save the probability model
# ===================================================

with open("markov_probabilities.json", "w") as f:
    json.dump(prob_model, f, indent=2)

print("\nSaved your trained Markov model → markov_probabilities.json")
