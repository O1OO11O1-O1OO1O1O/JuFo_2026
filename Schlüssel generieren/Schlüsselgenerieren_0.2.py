import RPi.GPIO as GPIO
from pathlib import Path
import time

GPIO.setmode(GPIO.BCM)
pfad = Path("/media/marten/INTENSO") / "zahlen.txt"
abc = ["A", "Ä", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "Ö", "P", "Q", "R", "S", "T", "U", "Ü", "V", "W", "X", "Y", "Z", "a", "ä", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "ö", "p", "q", "r", "s", "t", "u", "ü", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " ", "°"]

speicher = ""
sensor = 1

PIN_LDR1 = 17  

PIN_LDR2 = 27

PIN_NTC1 = 22


def LDR1():
    
    # Kondensator entladen
    GPIO.setup(PIN_LDR1, GPIO.OUT)
    GPIO.output(PIN_LDR1, GPIO.LOW)
    time.sleep(0.05)

    # Kondensator laden lassen
    GPIO.setup(PIN_LDR1, GPIO.IN)
    start_time = time.time()

    while GPIO.input(PIN_LDR1) == GPIO.LOW:
        pass

    return time.time() - start_time

def LDR2():
    
    # Kondensator entladen
    GPIO.setup(PIN_LDR2, GPIO.OUT)
    GPIO.output(PIN_LDR2, GPIO.LOW)
    time.sleep(0.05)

    # Kondensator laden lassen
    GPIO.setup(PIN_LDR2, GPIO.IN)
    start_time = time.time()

    while GPIO.input(PIN_LDR2) == GPIO.LOW:
        pass

    return time.time() - start_time

def NTC1():
    
    # Kondensator entladen
    GPIO.setup(PIN_NTC1, GPIO.OUT)
    GPIO.output(PIN_NTC1, GPIO.LOW)
    time.sleep(0.05)

    # Kondensator laden lassen
    GPIO.setup(PIN_NTC1, GPIO.IN)
    start_time = time.time()

    while GPIO.input(PIN_NTC1) == GPIO.LOW:
        pass

    return time.time() - start_time


try:

    while True:

        if sensor == 1:
            wert = str(LDR1())[-1]

        if sensor == 2:
            wert = str(LDR2())[-1]

        if sensor == 3:
            wert = str(NTC1())[-1]


        speicher = speicher + wert
        

        if len(speicher) == 2:

            wert = abc[int(speicher)] 
            print(wert)

            with pfad.open("a", encoding="utf-8") as f:

                f.write(wert)

            speicher = ""


        sensor += 1

        if sensor == 4:
            sensor = 1

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nProgramm beendet")
    GPIO.cleanup()
