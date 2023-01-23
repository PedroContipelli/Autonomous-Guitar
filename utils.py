import mido
from LookupTables import mute_tracks

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

# No loop for readability purposes
def string_of(note):
    if 40 <= note <= 44:
        return 'E'
    if 45 <= note <= 49:
        return 'A'
    if 50 <= note <= 54:
        return 'D'
    if 55 <= note <= 58:
        return 'G'
    if 59 <= note <= 63:
        return 'B'
    if 64 <= note <= 68:
        return 'e'
    return "ERROR: Note not in playable range"

def is_note_off(msg):
    return (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0)

def is_note_on(msg):
    return msg.type == 'note_on' and msg.velocity != 0

def is_note(msg):
    return msg.type.startswith('note')

def compress_outliers(note):
    while note > 68:
        note -= 12
    while note < 40:
        note += 12
    return note

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
