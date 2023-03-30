# servo : port
# CHANGE LEFT COLUMN ONLY

servo_to_port = {
    5 : 1,
    1 : 2,
    4 : 3,
    6 : 4,
    3 : 5,
    2 : 6,
    12 : 7,
    10 : 8,
    9 : 9,
    7 : 10,
    8 : 11,
    11 : 12,
    17 : 13,
    13 : 14,
    14 : 15,
    16 : 16,
    18 : 17,
    15 : 18,
    21 : 19,
    22 : 20,
    23 : 21,
    24 : 22,
    19 : 23,
    20 : 24,
    27 : 25,
    26 : 26,
    29 : 27,
    28 : 28,
    30 : 29,
    25 : 30
}

# All servo #s referred to below are VIRTUAL
servo_label = {
    6 : "e fret 1",
    5 : "B fret 1",
    4 : "G fret 1",
    3 : "D fret 1",
    2 : "A fret 1",
    1 : "E fret 1",
    12 : "e fret 2",
    11 : "B fret 2",
    10 : "G fret 2",
    9 : "D fret 2",
    8 : "A fret 2",
    7 : "E fret 2",
    18 : "e fret 3",
    17 : "B fret 3",
    16 : "G fret 3",
    15 : "D fret 3",
    14 : "A fret 3",
    13 : "E fret 3",
    24 : "e fret 4",
    23 : "B fret 4",
    22 : "G fret 4",
    21 : "D fret 4",
    20 : "A fret 4",
    19 : "E fret 4",
    25 : "Strum e",
    26 : "Strum B",
    27 : "Strum G",
    28 : "Strum D",
    29 : "Strum A",
    30 : "Strum E",
}

human_notes = {
    40 : "String 6 - Open   | E2",
    41 : "String 6 - Fret 1 | F2",
    42 : "String 6 - Fret 2 | F#2",
    43 : "String 6 - Fret 3 | G2",
    44 : "String 6 - Fret 4 | G#2",
    45 : "String 5 - Open   | A3",
    46 : "String 5 - Fret 1 | A#3",
    47 : "String 5 - Fret 2 | B3",
    48 : "String 5 - Fret 3 | C3",
    49 : "String 5 - Fret 4 | C#3",
    50 : "String 4 - Open   | D3",
    51 : "String 4 - Fret 1 | D#3",
    52 : "String 4 - Fret 2 | E3",
    53 : "String 4 - Fret 3 | F3",
    54 : "String 4 - Fret 4 | F#3",
    55 : "String 3 - Open   | G3",
    56 : "String 3 - Fret 1 | G#3",
    57 : "String 3 - Fret 2 | A4",
    58 : "String 3 - Fret 3 | A#4",
    59 : "String 2 - Open   | B4",
    60 : "String 2 - Fret 1 | C4",
    61 : "String 2 - Fret 2 | C#4",
    62 : "String 2 - Fret 3 | D4",
    63 : "String 2 - Fret 4 | D#4",
    64 : "String 1 - Open   | E4",
    65 : "String 1 - Fret 1 | F4",
    66 : "String 1 - Fret 2 | F#4",
    67 : "String 1 - Fret 3 | G4",
    68 : "String 1 - Fret 4 | G#4",
    0  : "None"
}

# Tracks that are unplayable on the guitar such as percussion, synth, etc
# Listed in reverse order for easier removal
mute_tracks = {
    "Africa" : [5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "Aladdin": [13, 10],
    "AllNotesTest": [],
    "CountryRoads": [10],
    "Mario": [],
    "Mii": [],
    "OverlappingNotesTest": [],
    "Pirates": [2], # Empty list to add "left hand" bass notes
    "Rickroll": [],
    "Simpsons": [16, 15],
    "StillDre": [],
    "Tetris": [],
    "TetrisModified": [],
    "Twinkle": [],
    "UnderTheSea": [1,2,3,4,5,6,7,8,9 , 11,12,13],
    "UnderTheSeaModified": [1,2,3,4,5,6,7,8,9 , 11,12,13],
    "VivaLaVida": []
}

slowdown_factor = {
    "Africa" : 1.25,
    "Aladdin": 1.3,
    "AllNotesTest": 3.0,
    "CountryRoads": 1.2,
    "Mario": 1.2,
    "Mii": 1.2,
    "OverlappingNotesTest": 1.2,
    "Pirates": 1.3,
    "Rickroll": 1.3,
    "Simpsons": 1.4,
    "StillDre": 1.2,
    "Tetris": 1.2,
    "TetrisModified": 1.1,
    "Twinkle": 1,
    "UnderTheSea": 1.2,
    "UnderTheSeaModified": 1.15,
    "VivaLaVida": 1.1
}

short_note_ticks = {
    "Africa" : 50,
    "Aladdin": 100,
    "AllNotesTest": 50,
    "CountryRoads": 40,
    "Mario": 50,
    "Mii": 50,
    "OverlappingNotesTest": 50,
    "Pirates": 50,
    "Rickroll": 100,
    "Simpsons": 50,
    "StillDre": 50,
    "Tetris": 50,
    "TetrisModified": 50,
    "Twinkle": 50,
    "UnderTheSea": 50,
    "UnderTheSeaModified": 50,
    "VivaLaVida": 30
}

# Note : [Fret Motor , String Motor]
play_servos = {
    40 : [0,30],
    41 : [1,30],
    42 : [7,30],
    43 : [13,30],
    44 : [19,30],
    45 : [0,29],
    46 : [2,29],
    47 : [8,29],
    48 : [14,29],
    49 : [20,29],
    50 : [0,28],
    51 : [3,28],
    52 : [9,28],
    53 : [15,28],
    54 : [21,28],
    55 : [0,27],
    56 : [4,27],
    57 : [10,27],
    58 : [16,27],
    59 : [0,26],
    60 : [5,26],
    61 : [11,26],
    62 : [17,26],
    63 : [23,26],
    64 : [0,25],
    65 : [6,25],
    66 : [12,25],
    67 : [18,25],
    68 : [24,25]
}
