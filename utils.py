import mido
from ESP32.LookupTables import mute_tracks

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

# Find minimum shift that maximizes the number of notes in our playable range
def find_best_shift(track):
    # Will store 2 * total times note n is played in note_counts[n] (1 for note_on & 1 for note_off)
    note_counts = [0 for i in range(120)]

    # Loop through song counting up all notes
    for msg in track:
        if msg.type.startswith('note'):
            note_counts[msg.note] += 1

    # Keep running sum of our note range size starting at note 0
    running_sum = sum(note_counts[0:29])
    running_sums = [running_sum]

    # Calculate sums of same range shifted by 1 each time
    for i in range(91):
        running_sums.append(running_sums[i] + note_counts[i+29] - note_counts[i])

    # 40 is the first note in our playable range
    # So best start note for range is the closest to 40 that maximizes notes played
    max_notes_played = max(running_sums)

    # Example for why sign is negated (-shift):
    # If best start note is 42, notes shift "down" by 2 so that 42 becomes 40
    for shift in range(25):
        if running_sums[40 + shift] == max_notes_played:
            return -shift
        if running_sums[40 - shift] == max_notes_played:
            return shift
    return "ERROR"

def remove_muted_tracks(input_filename, input_tracks):
    for mute_track in sorted(mute_tracks.get(input_filename, []), reverse=True):
        del input_tracks[mute_track]
    return input_tracks

def remove_short_notes(track, shorter_than_ticks):
    on_index = 0
    while on_index < len(track):
        on_msg = track[on_index]
        if is_note_on(on_msg):
            on_note = on_msg.note
            note_duration = 0
            off_index = on_index
            off_msg = track[off_index]
            while not (is_note_off(off_msg) and off_msg.note == on_note):
                off_index += 1
                off_msg = track[off_index]
                note_duration += off_msg.time

            if note_duration < shorter_than_ticks:
                track[off_index + 1].time += off_msg.time
                del track[off_index]
                track[on_index + 1].time += on_msg.time
                del track[on_index]
                continue
        on_index += 1
    return track
