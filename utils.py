def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

# For readability purposes
def string_of(note):
    if 40 <= note <= 44:
        return 6
    if 45 <= note <= 49:
        return 5
    if 50 <= note <= 54:
        return 4
    if 55 <= note <= 58:
        return 3
    if 59 <= note <= 63:
        return 2
    if 64 <= note <= 68:
        return 1
    return "ERROR: Note not in playable range"
