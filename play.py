from mido import MidiFile
from LookupTables import notes

for msg in MidiFile('MIDIs/Africa_Output.mid').play():
    print(msg)
    # print string from lookup table
