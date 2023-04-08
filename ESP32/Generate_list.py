import uos
def Midi_select():
    file = open('ESP32/midi_list.html', 'w')
    MIDI_list = uos.listdir('ESP32/Play_MIDIs')
    print(MIDI_list)
    cHTML = """
<HTML>

<HEAD>

<TITLE>Autonomous Guitar</TITLE>

</HEAD>

<BODY BGCOLOR="ADD8E6">

<HR>

<H1>Autonomous Guitar Project</H1>
<H2>By Senior Design Group 42</H2>

<label for="songs">Select a song:</label>

<select name="songs" id="songs">
"""
    file.write(cHTML)
    i = 1
    for s in MIDI_list:
        file.write("    <option value=\""+ str(s) + "\" href=\"/?" + str(s) + "\"></a>")
        file.write(s)
        file.write("</option>")
        file.write("\n")
        i = i + 1
    cHTML2 = """
</select>
<input type="submit" value="Submit" />
<br><br>

<label for="myfile">Select a file:</label>
<input type="file" id="myfile" name="myfile">
<button>Upload MIDI</button>

<br><br>
<a href="?play"><button>Play</button></a>
<button>Pause</button>
<button>Stop</button>

<HR>

</BODY>

</HTML>
"""
    file.write(cHTML2)
        
    file.close()