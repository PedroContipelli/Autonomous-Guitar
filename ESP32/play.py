import uos
uos.chdir('ESP32')

from Libraries.umidiparser import MidiFile, NOTE_ON
import utime
import time
from LookupTables import human_notes, servo_label, play_servos
from Servo_Controller import servo_write, alignment

play_file = "Twinkle_Output"
num_servos = 30
servo_states = [0] + [-1]*24 + [0]*6
last_fret_played_on = {25:0, 26:0, 27:0, 28:0, 29:0, 30:0}

def main():
    alignment()
    time.sleep(5)
    
    for msg in MidiFile(f"Play_MIDIs/{play_file}.mid").play():
        if msg.status == NOTE_ON:
            play_guitar_note(note=msg.note, print_human_notes=True, debug=False)

def play_guitar_note(note, print_human_notes=False, debug=False):
    
    if print_human_notes:
        print("Playing", human_notes[note])

    new_fret, new_strum = play_servos[note]
    old_fret = last_fret_played_on[new_strum]

    # Fret up or release every motor on this note's string
    for fret in range((30 - new_strum), 24, 6):
        fret += 1 # Adjusts for 1-indexed servos
        
        # RELEASE (-1) <- UP (0) <- DOWN (1)
        if servo_states[fret] > -1:
            servo_states[fret] -= 1
        
    # Fret down the motor for this note
    servo_states[new_fret] = 1
                
    # IDEA: FRET MOTORS ARE CLOSE TO FRETS AND STRUMS NEED LARGER ANGLE TO REACH
    # PROVIDES MECHANICAL DELAY FOR FRETTING BEFORE STRUMMING

    # STRUM
    servo_states[new_strum] = 1 - servo_states[new_strum]
    if debug:
        print(f"{servo_label[new_strum]} (Motor # {new_strum})\n")

    # Update last note played
    last_fret_played_on[new_strum] = new_fret

    # WRITE ALL SERVOS
    servo_write(servo_states)

if __name__ == "__main__":
    main()

