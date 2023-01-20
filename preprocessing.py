import mido
from LookupTables import notes, mute_tracks
from utils import clamp

# input_filenames = ['Africa']
input_filenames = ['Africa', 'Aladdin', 'AllNotesTest', 'CountryRoads', 'Mii', 'OverlappingNotesTest', 'Pirates', 'Rickroll', 'Simpsons', 'StillDre', 'Tetris', 'Twinkle', 'UnderTheSea', 'VivaLaVida']
# input_filenames = ['Mario']

# Find shift that minimizes the number of notes outside of our playable range
def find_best_shift(track):
    note_counts = [0 for i in range(100)]

    for msg in track:
        if msg.type.startswith('note'):
            note_counts[msg.note] += 1

    running_sum = sum(note_counts[0:29])
    running_sums = [running_sum]

    for i in range(71):
        running_sums.append(running_sums[i] + note_counts[i+29] - note_counts[i])

    best_range_start = running_sums.index(max(running_sums))
    best_shift = 40 - best_range_start # 40 is the first note in our playable range
    # print("Best shift:", best_shift)
    return best_shift

def remove_muted_tracks(input_filename, input_tracks):
    for mute_track in mute_tracks.get(input_filename):
        del input_tracks[mute_track]
    return input_tracks

for input_filename in input_filenames:
    print(f'Preprocessing {input_filename}...')
    input_file = mido.MidiFile(f'./MIDIs/{input_filename}.mid')

    all_tracks = mido.merge_tracks(input_file.tracks)
    best_shift = find_best_shift(all_tracks)

    kept_tracks = remove_muted_tracks(input_filename, input_file.tracks)
    input_track = mido.merge_tracks(kept_tracks)

    output_track = mido.MidiTrack()
    # Set instrument to "acoustic guitar (steel string)"
    output_track.append(mido.Message(type='program_change', channel=0, program=25, time=0))

    note_states = [False for i in range(100)]

    for msg in input_track:
        if msg.type.startswith('note'):
            # Shift all notes to maximize notes in playable range
            msg.note += best_shift

            # Outlier notes compression into playable range (E2 - G#4)
            while msg.note > 68:
                msg.note -= 12
            while msg.note < 40:
                msg.note += 12

            # Set all notes to same instrument channel
            msg.channel = 0

            if msg.type == 'note_on' and note_states[msg.note]:
                    output_track.append(mido.Message('note_off', channel=0, note=msg.note, velocity=0, time=msg.time))
                    msg.time = 0 # Starting new note where previous ended

            note_states[msg.note] = (msg.type == 'note_on')

        # Skip any instructions to change instrument
        if msg.type == 'program_change':
            continue

        output_track.append(msg)

    output_file = mido.MidiFile()
    slowdown_factor = 1
    output_file.ticks_per_beat = int(input_file.ticks_per_beat / slowdown_factor)

    output_file.tracks.append(output_track)
    output_file.save(f'./MIDIs/{input_filename}_Output.mid')
