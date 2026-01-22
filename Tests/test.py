from music21 import stream, chord, note
import random
import os

# -----------------------------
# Step 1: Base chord functions and tension
# -----------------------------
base_functions = {
    "C": ("Tonic", 1.0),
    "Am": ("Tonic", 1.0),
    "F": ("Predominant", 2.0),
    "G": ("Dominant", 3.0),
    "D": ("Secondary Dominant (V/V)", 3.5),
    "E": ("Secondary Dominant (V/vi)", 3.5),
    "A": ("Secondary Dominant (V/ii)", 3.5)
}

# -----------------------------
# Step 2: Next chord rules
# -----------------------------
next_chord_map = {
    "Tonic": ["F", "G", "C"],
    "Predominant": ["G", "C"],
    "Dominant": ["C", "D", "E", "A"],
    "Secondary Dominant (V/V)": ["G"],
    "Secondary Dominant (V/vi)": ["Am"],
    "Secondary Dominant (V/ii)": ["D"]
}

# -----------------------------
# Step 3: Chord tension adjustment for 7th/9th/13th
# -----------------------------
def tension_with_extensions(chord_name, base_tension):
    if chord_name in ["G", "D", "E", "A"]:  # Dominants + secondary dominants
        return base_tension + 1.0
    elif chord_name in ["C", "Am", "F"]:    # Tonic/Predominant color notes
        return base_tension + 0.5
    else:
        return base_tension

# -----------------------------
# Step 4: User input
# -----------------------------
user_input = input("Enter starting chord (C, Am, F, G, etc.): ").strip()
# Normalize input: first letter uppercase, keep 'm' if minor
if len(user_input) > 1 and user_input[1].lower() == "m":
    start_chord = user_input[0].upper() + "m"
else:
    start_chord = user_input[0].upper()

# Fallback if chord not recognized
if start_chord not in base_functions:
    print(f"⚠️ Warning: '{start_chord}' not recognized. Using 'C' instead.")
    start_chord = "C"

length = int(input("Enter desired progression length: "))

# Use W/S/D instead of arrows
desired_curve_input = input(
    "Enter tension curve using W=up, S=down, D=neutral (e.g., WDSD): "
).strip().upper()

# Map to internal arrows for processing
tension_curve = []
for ch in desired_curve_input:
    if ch == "W":
        tension_curve.append("↑")
    elif ch == "S":
        tension_curve.append("↓")
    elif ch == "D":
        tension_curve.append("→")
    else:
        print(f"⚠️ Warning: '{ch}' not recognized. Using neutral (→).")
        tension_curve.append("→")

# Color layer toggle (the only optional feature left)
use_extensions_input = input("Do you want extra chord color (7th/9th/13th)? (y/n): ").strip().lower()
use_extensions = True if use_extensions_input == "y" else False

# -----------------------------
# Step 5: Generate chord progression
# -----------------------------
progression = [start_chord]

for i in range(1, length):
    current_chord = progression[-1]
    function, base_tension = base_functions.get(current_chord, ("Unknown", 0.0))
    total_tension = tension_with_extensions(current_chord, base_tension)

    allowed = next_chord_map.get(function, [])

    # Filter allowed chords by tension curve
    if i-1 < len(tension_curve):
        change = tension_curve[i-1]
        filtered = []
        for chord_name in allowed:
            _, next_base = base_functions.get(chord_name, ("Unknown", 0.0))
            next_tension = tension_with_extensions(chord_name, next_base)
            if change == "↑" and next_tension > total_tension:
                filtered.append(chord_name)
            elif change == "↓" and next_tension < total_tension:
                filtered.append(chord_name)
            elif change == "→" and abs(next_tension - total_tension) <= 0.2:
                filtered.append(chord_name)
        allowed = filtered

    # Fallbacks to avoid empty list
    if not allowed:
        allowed = next_chord_map.get(function, [])
        if not allowed:
            allowed = list(base_functions.keys())

    next_chord = random.choice(allowed)
    progression.append(next_chord)

print("\nGenerated chord progression:")
print(" → ".join(progression))

# -----------------------------
# Step 6: Chord mapping with optional color layer
# -----------------------------
triad_map = {
    "C": ["C4", "E4", "G4"],
    "Am": ["A3", "C4", "E4"],
    "F": ["F3", "A3", "C4"],
    "G": ["G3", "B3", "D4"],
    "D": ["D3", "F#3", "A3"],
    "E": ["E3", "G#3", "B3"],
    "A": ["A3", "C#4", "E4"]
}

chord_color_map = {
    "C": ["C4", "E4", "G4", "B4", "D5", "A4"],      
    "Am": ["A3", "C4", "E4", "G4", "B4", "D5"],     
    "F": ["F3", "A3", "C4", "E4", "G4", "D5"],      
    "G": ["G3", "B3", "D4", "F4", "A4", "E5"],      
    "D": ["D3", "F#3", "A3", "C4", "E4", "B4"],     
    "E": ["E3", "G#3", "B3", "D4", "F#4", "C#5"],   
    "A": ["A3", "C#4", "E4", "G4", "B4", "F#4"]     
}

# -----------------------------
# Step 7: Export MIDI
# -----------------------------
s = stream.Stream()
chord_duration = 4  # quarter notes

for ch_name in progression:
    if use_extensions:
        notes_list = [note.Note(p) for p in chord_color_map.get(ch_name, ["C4","E4","G4"])]
    else:
        notes_list = [note.Note(p) for p in triad_map.get(ch_name, ["C4","E4","G4"])]
    c = chord.Chord(notes_list)
    c.quarterLength = chord_duration
    s.append(c)

midi_file_name = os.path.join(os.getcwd(), "generated_progression_final.mid")
s.write('midi', fp=midi_file_name)
print(f"\n✅ MIDI exported to: {midi_file_name}")
