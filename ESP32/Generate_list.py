import uos
def Midi_select():
    file = open('ESP32/midi_list.html', 'w')
    MIDI_list = uos.listdir('ESP32/Play_MIDIs')
    print(MIDI_list)
    cHTML = """
<HTML>

<HEAD>

<TITLE>Self-Playing Guitar</TITLE>

</HEAD>

<BODY BGCOLOR="ADD8E6">

<HR>

<H1>Self-Playing Guitar Project</H1>
<H2>By Senior Design Group 30</H2>

<label for="songs">Select a song:</label>

<select name="songs" id="songs">
"""
    file.write(cHTML)
    file.write("\n")
    file.write("    <option value=\"Song Select\" href=\"/Song select\"></a>")
    file.write("\n")
    i = 1
    for s in MIDI_list:
        file.write("    <option value=\""+ str(s) + "\" href=\"/?" + str(s) + "\"></a>")
        print("    <option value=\""+ str(s) + "\" href=\"/?" + str(s) + "\"></a>")
        file.write(s)
        file.write("</option>")
        file.write("\n")
        i = i + 1
    cHTML2 = """
</select>
<br><br>
<script>
    document.getElementById("songs").onchange = function() {
        if (this.selectedIndex !== 0) {
            window.location.href = this.value;
        }
    };
    
    
</script>

<br><br>
<a href="?play"><button>Play</button></a>


<HR>

</BODY>

</HTML>
"""
    file.write(cHTML2)
        
    file.close()