from music21 import stream, harmony, midi
import random

# ----------------------------
# Functional harmony knowledge
# ----------------------------

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

# ----------------------------
# Extensions (color layer)
# ----------------------------

EXTENSIONS = {
    "tonic": ["", "7", "9"],
    "predominant": ["", "7", "9"],
    "dominant": ["", "7", "9"]
}

# ----------------------------
# Helpers
# ----------------------------

def normalize(ch):
    ch = ch.strip()
    if len(ch) == 1:
        return ch.upper()
    return ch[0].upper() + ch[1:].lower()

def strip_extension(ch):
    return ch.replace("7", "").replace("9", "")

def get_function(ch):
    return FUNCTIONS.get(strip_extension(ch), "tonic")

def get_mood(ch):
    return MOOD_BY_FUNCTION[get_function(ch)]

def apply_extension(ch, allow_ext):
    if not allow_ext:
        return ch
    func = get_function(ch)
    ext = random.choice(EXTENSIONS[func])
    return ch + ext

# ----------------------------
# Suggestion engine
# ----------------------------

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

    # fallback if mood filter too strict
    if not candidates:
        for ch in KEY_CHORDS:
            if get_function(ch) in target_funcs:
                candidates.append(ch)

    return candidates

# ----------------------------
# MIDI rendering (FIXED)
# ----------------------------

def render_midi(progression):
    s = stream.Stream()
    for ch in progression:
        cs = harmony.ChordSymbol(ch)
        cs.quarterLength = 2
        s.append(cs)

    mf = midi.translate.streamToMidiFile(s)
    mf.open("final_progression.mid", "wb")
    mf.write()
    mf.close()

# ----------------------------
# INTERACTIVE SESSION
# ----------------------------

print("\nStep-by-step Interactive Next-Chord AI (music21)")
use_ext = input("Include chord extensions (7/9)? (y/n): ").lower().startswith("y")

print("\nPreferred mood direction:")
print("1: tension / drive")
print("2: stable / floating")
print("3: release / relief")
print("4: mixed")
mood_choice = input("> ")

MOOD_MAP = {
    "1": "tension / drive",
    "2": "stable / floating",
    "3": "release / relief",
    "4": "mixed"
}

preferred_mood = MOOD_MAP.get(mood_choice, "mixed")

export_midi = input("\nExport MIDI at the end? (y/n): ").lower().startswith("y")

start = normalize(input("\nEnter starting chord (C, Am, F, etc.): "))
progression = [apply_extension(start, use_ext)]

while True:
    prev = strip_extension(progression[-1])
    suggestions = suggest_next(prev, preferred_mood)

    if not suggestions:
        print("No continuation available.")
        break

    print("\nNext chord suggestions:")
    for i, ch in enumerate(suggestions, 1):
        print(f"{i}: {ch} | mood: {get_mood(ch)}")

    choice = input("> Enter chord, number, or 'done': ").strip()

    if choice.lower() == "done":
        break

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(suggestions):
            next_ch = suggestions[idx]
        else:
            print("Invalid number.")
            continue
    else:
        next_ch = normalize(choice)
        if next_ch not in KEY_CHORDS:
            print("Invalid chord.")
            continue

    progression.append(apply_extension(next_ch, use_ext))

# ----------------------------
# Final output
# ----------------------------

print("\nFinal progression:")
print(" → ".join(progression))

if export_midi:
    render_midi(progression)
    print("\nMIDI file saved as final_progression.mid")
