import mido, utils

test_file = 'Twinkle'
input_file = mido.MidiFile(f'MIDIs/{test_file}.mid')

def debug_print(msg):
    if utils.is_note_off(msg):
        print("NOTE OFF:", msg.note, f"-- ({msg})")
    elif utils.is_note_on(msg):
        print("NOTE ON: ", msg.note, f"-- ({msg})")
    else:
        print(msg)

print("\n======================================================\nINPUT:\n======================================================\n")
for track in input_file.tracks:
    i = 0
    for msg in track:
        debug_print(msg)
        i += 1
        if i >= 100:
            break

output_file = mido.MidiFile(f'MIDIs/{test_file}_Output.mid')

print("\n======================================================\nOUTPUT:\n======================================================\n")
for track in output_file.tracks:
    i = 0
    for msg in track:
        debug_print(msg)
        i += 1
        if i >= 100:
            break



'''
for track in input_file.tracks:
    for msg in track:
        if msg.type.startswith('note'):
'''
