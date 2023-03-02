import uos
uos.chdir('ESP32')

import umidiparser
import utime
from LookupTables import human_notes, servo_label, play_servos
from Servo_Controller import servo_write

play_file = "Twinkle_Output"
num_servos = 30
servo_states = [0 for i in range(num_servos + 1)]
previous_states = servo_states.copy()
last_fret_played_on = {25:0, 26:0, 27:0, 28:0, 29:0, 30:0}

def main():
    for msg in umidiparser.MidiFile(f"MIDIs/{play_file}.mid").play():
        if msg.status == umidiparser.NOTE_ON:
            play_guitar_note(note=msg.note, print_human_notes=True, debug=False)

def play_guitar_note(note, print_human_notes=False, debug=False):
    
    if print_human_notes:
        print("Playing", human_notes[note])

    fret_motor, strum_motor = play_servos[note]
    previous_fret = last_fret_played_on[strum_motor]

    if previous_fret != fret_motor:
        # UNFRET OLD
        if previous_fret != 0:
            servo_states[previous_fret] = 0
            if debug:
                print(f"OFF {servo_label[previous_fret]} (Motor # {previous_fret})")

        # FRET NEW
        if fret_motor != 0:
            servo_states[fret_motor] = 1
            if debug:
                print(f"ON {servo_label[fret_motor]} (Motor # {fret_motor})")

    # STRUM
    servo_states[strum_motor] = 1 - servo_states[strum_motor]
    if debug:
        print(f"{servo_label[strum_motor]} (Motor # {strum_motor})\n")

    # Update last note played
    last_fret_played_on[strum_motor] = fret_motor

    # WRITE ALL SERVOS
    previous_states_local = servo_write(servo_states, previous_states)
    
    for i in range(len(previous_states_local)):
        previous_states[i] = previous_states_local[i]

if __name__ == "__main__":
    main()
