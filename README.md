# [Self-Playing Guitar](https://pedrocontipelli.github.io/Autonomous-Guitar/)

An autonomous guitar that takes in MIDI files as input and plays them live on an acoustic guitar using servo motors.
By: Pedro Contipelli, Blake Cannoe, Ethan Partidas, Kyle Walker, Jon Catala

## Project Summary (200 words)
The goal of this project is to create a fully autonomous robotic guitar that can use its motors to play any song that is inputted to the system (both strumming and fretting). We hope to bridge the gap between art and engineering, as well as foster interest in STEM fields using music: a universal language that anyone can appreciate. It works by using a custom algorithm running in Python on a microcontroller to take in music data and precisely time the outputs of various servo motors (which are mounted on the acoustic guitar) to play the given song. It's very difficult to find other projects that do this, and existing ones tend to be quite expensive ($1000+) whereas we believe we can fit our entire scope under a budget of $400. Although the project's main application is for entertainment, it can also be used as a teaching instrument for both music and engineering design principles!

Preprocessing performed on a computer using mido Python3 library
(https://mido.readthedocs.io/)

Playing performed on ESP32 using umidiparser MicroPython library
(https://github.com/bixb922/umidiparser)

**Workflow:**
1. `pip3 install mido`
2. Clone git repo `https://github.com/ethanpartidas/Autonomous-Guitar.git`
4. Find folder and `cd Autonomous-Guitar` into it
5. Run `preprocessing.py`
6. In Thonny, Enable: View > Files
7. Transfer `ESP32` folder over to microcontroller
8. Run `ESP32/play.py` from MicroPython Device

**Youtube Links:**
CDR Presentation: https://youtu.be/u37AItDfGn4
Midterm Demo: https://youtu.be/ydaQEmD9ljA
Final Demo(s):

University of Central Florida - Senior Design Project (Spring 2023)
Under supervision of: Richard Leinecker (CS) and Samuel Richie (ECE)
