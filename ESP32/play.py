import uos
uos.chdir('ESP32')

from Libraries.umidiparser import MidiFile, NOTE_ON
import utime
import time
from LookupTables import human_notes, servo_label, play_servos
from Servo_Controller import servo_write, alignment

play_file = "TetrisModified_Output"
num_servos = 30
servo_states = [0] + [-1]*24 + [0]*6
timeouts = [0 for i in range(num_servos-6+1)]
delay_ms = 500
last_fret_played_on = {25:0, 26:0, 27:0, 28:0, 29:0, 30:0}

def main():
    alignment()
    time.sleep(2)
    
    for msg in MidiFile(f"Play_MIDIs/{play_file}.mid").play():
        if msg.status == NOTE_ON:
            play_guitar_note(note=msg.note, print_human_notes=True, debug=False)

    time.sleep(3)
    event_queue_timeout_check()

def play_guitar_note(note, print_human_notes=False, debug=False):
    
    if print_human_notes:
        print("Playing", human_notes[note])

    new_fret, new_strum = play_servos[note]
    old_fret = last_fret_played_on[new_strum]

    event_queue_timeout_check()
    
    # Fret up every motor on this note's string so correct note plays
    for fret in range((30 - new_strum), 24, 6):
        fret += 1 # Adjusts for 1-indexed servos
        
        if servo_states[fret] == 1:
            servo_states[fret] = 0

    # Fret down the motor for this note
    servo_states[new_fret] = 1
    timeouts[new_fret] = time.ticks_ms() + delay_ms
                
    # IDEA: FRET MOTORS ARE CLOSER TO FRETS AND STRUMS NEED LARGER ANGLE TO REACH
    # PROVIDES MECHANICAL DELAY FOR FRETTING BEFORE STRUMMING

    # STRUM
    servo_states[new_strum] = 1 - servo_states[new_strum]
    if debug:
        print(f"{servo_label[new_strum]} (Motor # {new_strum})\n")

    # Update last note played
    last_fret_played_on[new_strum] = new_fret

    # WRITE ALL SERVOS
    servo_write(servo_states)

def event_queue_timeout_check():
    global servo_states
    current_time = time.ticks_ms()
    for fret_servo in range(1, (num_servos-6) +1):
        if current_time >= timeouts[fret_servo] and timeouts[fret_servo] != 0:
            if servo_states[fret_servo] == 1:
                servo_states[fret_servo] = 0
                timeouts[fret_servo] += delay_ms
            elif servo_states[fret_servo] == 0:
                servo_states[fret_servo] = -1
                timeouts[fret_servo] = 0

if __name__ == "__main__":
    main()