import mido
from LookupTables import notes
from utils import clamp, string_of, is_note_off, is_note_on, compress_outliers, find_best_shift, remove_muted_tracks, remove_short_notes

input_filenames = ['Africa', 'Aladdin', 'AllNotesTest', 'CountryRoads', 'Mii', 'OverlappingNotesTest', 'Pirates', 'Rickroll', 'Simpsons', 'StillDre', 'Tetris', 'Twinkle', 'UnderTheSea', 'VivaLaVida']
# input_filenames = ['Mario']

for input_filename in input_filenames:
    print(f'Preprocessing {input_filename}...')
    input_file = mido.MidiFile(f'./MIDIs/{input_filename}.mid')

    all_tracks = mido.merge_tracks(input_file.tracks)
    best_shift = find_best_shift(all_tracks)

    kept_tracks = remove_muted_tracks(input_filename, input_file.tracks)
    input_track = mido.merge_tracks(kept_tracks)

    output_track = mido.MidiTrack()
    # [Program=25] sets instrument to "acoustic guitar (steel string)"
    output_track.append(mido.Message(type='program_change', channel=0, program=25, time=0))

    # Strings indexed as per musical convention (e B G D A E)
    last_note_played_on = {'e':0, 'B':0, 'G':0, 'D':0, 'A':0, 'E':0}
    time_accumulated = 0

    for msg in input_track:
        # Skip unplayable instructions (instrument, volume, pitch bending, note_off)
        if msg.type in ['program_change', 'control_change', 'pitchwheel'] or is_note_off(msg):
            time_accumulated += msg.time
            continue

        if is_note_on(msg):
            msg.note += best_shift # Shift all notes to maximize amount in playable range (E2 - G#4)
            msg.note = compress_outliers(msg.note) # Any leftover notes raised/lowered in octaves to fit
            msg.channel = 0 # Set all notes to same instrument channel

            # Force end last note on current string so new note can be played
            guitar_string = string_of(msg.note)
            turn_off = mido.Message('note_off')
            turn_off.note = last_note_played_on[guitar_string]
            turn_off.time = msg.time + time_accumulated
            output_track.append(turn_off)

            # Reset for current note
            msg.time = 0
            time_accumulated = 0
            last_note_played_on[guitar_string] = msg.note

        # Add current instruction to output
        output_track.append(msg)

    # End final notes
    for off_note in last_note_played_on.values():
        output_track.append(mido.Message('note_off', note=off_note, time=200))

    output_track = remove_short_notes(output_track, shorter_than_ticks=50)

    output_file = mido.MidiFile()
    slowdown_factor = 1
    output_file.ticks_per_beat = int(input_file.ticks_per_beat / slowdown_factor)

    output_file.tracks.append(output_track)
    output_file.save(f'./MIDIs/{input_filename}_Output.mid')
