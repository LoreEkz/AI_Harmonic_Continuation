import json
from collections import defaultdict

# ------------------------------------------------------
# Load dataset
# ------------------------------------------------------

with open("chords_dataset.json", "r") as f:
    data = json.load(f)

# ------------------------------------------------------
# Prepare model structure
# ------------------------------------------------------
# model[mood][(func1, func2)][next_func] = count

model = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

FUNCTIONS = {
    "C": "tonic", "Am": "tonic", "Em": "tonic",
    "F": "predominant", "Dm": "predominant",
    "G": "dominant", "Bdim": "dominant",
}

def get_function(ch):
    return FUNCTIONS.get(ch, "tonic")

print("Counting 2nd-order transitions...")

for sample in data:
    mood = sample["mood"]
    func_seq = sample["functions"]
    next_chord = sample["next_chord"]
    next_func = get_function(next_chord)

    if len(func_seq) < 2:
        continue

    prev2 = func_seq[-2]
    prev1 = func_seq[-1]

    key = (prev2, prev1)

    model[mood][key][next_func] += 1

print("2nd-order training complete.")

# ------------------------------------------------------
# Normalize counts → probabilities
# ------------------------------------------------------

prob_model = defaultdict(dict)

print("Normalizing...")

for mood in model:
    prob_model[mood] = {}
    for key_tuple in model[mood]:
        total = sum(model[mood][key_tuple].values())
        prob_model[mood][key_tuple] = {}

        for next_func, count in model[mood][key_tuple].items():
            prob_model[mood][key_tuple][next_func] = count / total

print("Normalization complete.")

# ------------------------------------------------------
# Save model (tuple keys → strings)
# ------------------------------------------------------

def encode_key(key_tuple):
    return f"{key_tuple[0]}|{key_tuple[1]}"

encoded_model = {}

for mood, transitions in prob_model.items():
    encoded_model[mood] = {}
    for key_tuple, next_probs in transitions.items():
        encoded_key = encode_key(key_tuple)
        encoded_model[mood][encoded_key] = next_probs

with open("markov_probabilities_2nd_order.json", "w") as f:
    json.dump(encoded_model, f, indent=2)

print("\nSaved: markov_probabilities_2nd_order.json")

