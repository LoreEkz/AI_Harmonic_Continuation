AI Harmonic Continuation Model
An interactive, mood-conditioned harmonic prediction system built on functional harmony and a 2nd-order Markov model.


🎶 Overview

This project implements an AI-assisted chord progression continuation engine designed for music producers and composers.
Unlike black-box deep learning models, this system uses:

- Functional harmony (tonic / predominant / dominant)
- Mood conditioning (stable, motion, tension)
- Rule-based dataset generation
- 1st & 2nd order Markov models
- Interactive and automatic chord generation modes

The goal is to create a transparent, controllable, and musically coherent harmonic engine that can later evolve into LSTM/Transformer architectures.


🧠 Why This Project?

Current AI music models often:
❌ lack interpretability
❌ break harmonic rules
❌ ignore functional context
❌ generate random-sounding progressions

This project focuses on:

✔️ structure first,
✔️ machine learning later.

By grounding everything in functional harmony, we get:

- predictable behavior
- real musical logic
- directional harmonic movement
- controllable outputs
- explainable decisions


📚 Features
✓ Functional Harmony Engine

Tonic / Predominant / Dominant classification
Reduced complexity → increased learnability

✓ Mood Conditioning

stable / floating (tonic)
gentle motion (predominant)
tension / drive (dominant)

✓ Synthetic Rule-Based Dataset

Copyright-free
Fully controlled
Thousands of harmonic transitions

✓ Markov Models

2nd-order for realistic chord transitions
1st-order fallback
Probability distributions conditioned on mood

✓ Generation Modes

Automatic mode → generate full progressions
Interactive mode → producer chooses each next chord with ranked suggestions


⚙️ Installation

Clone the repository:
git clone git@github.com:LoreEkz/AI_Harmonic_Continuation.git
cd AI_Harmonic_Continuation

Install dependencies:
pip install -r requirements.txt


▶️ Usage
Interactive Mode

Pick the next chord with real-time suggestions:

python interactive_markov_2nd_order.py
- Automatic Progression Generation

Generate full progressions of any length:
- python generate_with_markov_2nd_order.py
- Dataset Generation

Rebuild the full synthetic dataset:
- python generate_dataset_no_ext.py

📊 Project Architecture
functional harmony → synthetic dataset → Markov model → chord generator
      ↑                                               ↓
    mood labels ←———————— interactive loop —————————→ user choices

📁 Repository Structure (after cleanup)
AI_Harmonic_Continuation/
│
├── data/                    # datasets & probability maps
│   ├── chords_dataset.json
│   ├── markov_probabilities.json
│   └── markov_probabilities_2nd_order.json
│
├── models/                  # training + Markov implementations
│   ├── markov_training.py
│   ├── markov_training_2nd_order.py
│   ├── generate_markov.py
│   └── generate_markov_2nd_order.py
│
├── interactive/             # user-facing generation tools
│   └── interactive_markov_2nd_order.py
│
├── tests/                   # test scripts & experimental files
│
├── utils/                   # harmony logic, mood mappings
│   ├── harmony_rules.py
│   └── mood_map.py
│
├── requirements.txt
├── README.md
└── LICENSE (optional)


🔭 Future Work

- Harmonic Enhancements
- Inversions & voice leading
- Chord extensions
- Borrowed chords / chromaticism
- Secondary dominants
- Machine Learning Extensions
- LSTM / Transformer version
- Embedding-based harmonic representation
- Reinforcement learning from user choices
- System Extensions
- Real-time MIDI input
- DAW plugin (VST / AU)
- Style conditioning (pop, ambient, EDM)
