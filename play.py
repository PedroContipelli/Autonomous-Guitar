import mido, utils
from LookupTables import human_notes, servo_label, play_servos

play_file = "Twinkle_Output"

servo_state = [False for i in range(31)]
last_fret_played_on = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

def play_guitar_note(msg, print_human_notes=False, debug=False):

    fret_motor, strum_motor = play_servos[msg.note]
    previous_fret = last_fret_played_on[strum_motor]

    if previous_fret != fret_motor:
        # UNFRET OLD
        if previous_fret != 0:
            servo_state[previous_fret] = False
            if debug:
                print(f"OFF {servo_label[previous_fret]} (Motor # {previous_fret})")

        # FRET NEW
        if fret_motor != 0:
            servo_state[fret_motor] = True
            if debug:
                print(f"ON {servo_label[fret_motor]} (Motor # {fret_motor})")

    # STRUM
    servo_state[strum_motor] = not servo_state[strum_motor]
    if debug:
        print(f"{servo_label[strum_motor]} (Motor # {strum_motor})\n")

    # Update last note played
    last_fret_played_on[strum_motor] = fret_motor

    if print_human_notes:
        print("Playing", human_notes[msg.note])

for msg in mido.MidiFile(f"MIDIs/{play_file}.mid").play():
    if utils.is_note_on(msg):
        play_guitar_note(msg, print_human_notes=True, debug=False)
