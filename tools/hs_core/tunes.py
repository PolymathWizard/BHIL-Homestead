"""Tune library for click-to-play tracks.

ode-to-joy      Beethoven, Symphony No. 9 theme (1824). Public-domain composition,
                sequenced fresh for HOMESTEAD.
homestead-riff  Original melody written for HOMESTEAD, CC BY 4.0.
"""

TUNES = {
    "ode-to-joy": {
        "bpm": 132,
        "credit": "Ludwig van Beethoven, Ode to Joy theme (public domain composition), sequenced for HOMESTEAD",
        "notes": [
            ("E5", 1), ("E5", 1), ("F5", 1), ("G5", 1),
            ("G5", 1), ("F5", 1), ("E5", 1), ("D5", 1),
            ("C5", 1), ("C5", 1), ("D5", 1), ("E5", 1),
            ("E5", 1.5), ("D5", 0.5), ("D5", 2),
            ("E5", 1), ("E5", 1), ("F5", 1), ("G5", 1),
            ("G5", 1), ("F5", 1), ("E5", 1), ("D5", 1),
            ("C5", 1), ("C5", 1), ("D5", 1), ("E5", 1),
            ("D5", 1.5), ("C5", 0.5), ("C5", 2),
        ],
    },
    "homestead-riff": {
        "bpm": 140,
        "credit": "Original HOMESTEAD melody, CC BY 4.0",
        "notes": [
            ("C5", 0.5), ("E5", 0.5), ("G5", 0.5), ("E5", 0.5), ("A5", 0.5), ("G5", 0.5), ("E5", 0.5), ("C5", 0.5),
            ("D5", 0.5), ("F5", 0.5), ("A5", 0.5), ("F5", 0.5), ("G5", 1), ("R", 1),
            ("C5", 0.5), ("E5", 0.5), ("G5", 0.5), ("C6", 0.5), ("B5", 0.5), ("G5", 0.5), ("E5", 0.5), ("D5", 0.5),
            ("E5", 0.5), ("D5", 0.5), ("C5", 1), ("G4", 1), ("C5", 1),
        ],
    },
}
