# Autonomous-Guitar
An autonomous guitar that takes in MIDI files as input and plays them live on an acoustic guitar using servo motors.

Preprocessing performed on a computer using mido Python3 library
(https://mido.readthedocs.io/)

Playing performed on ESP32 using umidiparser MicroPython library
(https://github.com/bixb922/umidiparser)

**Workflow:**
1. `pip3 install mido`
2. Clone git repo `https://github.com/ethanpartidas/Autonomous-Guitar.git`
4. Find folder and `cd Autonomous-Guitar` into it
5. Run `preprocessing.py`
6. `ampy --port COM3 put ESP32`  (might take 2-3 mins, folder contains all used files)
7. Run `ESP32/play.py` from MicroPython Device
