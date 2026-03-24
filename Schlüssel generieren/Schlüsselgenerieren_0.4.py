import RPi.GPIO as GPIO
from pathlib import Path
import time

GPIO.setmode(GPIO.BCM)

KeySets = 100 #Einstellen!!!
intervall = 0.1
name = "test-2_" + str(intervall) + ".txt"
länge = 0
speicher = ""
sensor = 0
pfad = Path("/home/marten/Test Schlüssel") / name # Path("/media/marten/INTENSO") / "zahlen.txt"
abc = ["A", "Ä", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "Ö", "P", "Q", "R", "S", "T", "U", "Ü", "V", "W", "X", "Y", "Z", "a", "ä", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "ö", "p", "q", "r", "s", "t", "u", "ü", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " ", "°"]

PIN_LDR1 = 17  
PIN_LDR2 = 27
PIN_NTC1 = 22

#print("Dauer: ca.", KeySets * 240 / ((1 / intervall + 0.05) * 60), "Minuten")


def LDR1():
    
    counter = 0

    for x in range(5):

        GPIO.setup(PIN_LDR1, GPIO.OUT)
        GPIO.output(PIN_LDR1, GPIO.LOW)
        time.sleep(0.05)

        GPIO.setup(PIN_LDR1, GPIO.IN)

        while GPIO.input(PIN_LDR1) == GPIO.LOW:

            counter = (counter + 1) % 10

    return counter

def LDR2():
    
    counter = 0

    for x in range(5):

        GPIO.setup(PIN_LDR2, GPIO.OUT)
        GPIO.output(PIN_LDR2, GPIO.LOW)
        time.sleep(0.05)

        GPIO.setup(PIN_LDR2, GPIO.IN)

        while GPIO.input(PIN_LDR2) == GPIO.LOW:

            counter = (counter + 1) % 10

    return counter

def NTC1():
    
    counter = 0

    for x in range(5):

        GPIO.setup(PIN_NTC1, GPIO.OUT)
        GPIO.output(PIN_NTC1, GPIO.LOW)
        time.sleep(0.05)

        GPIO.setup(PIN_NTC1, GPIO.IN)

        while GPIO.input(PIN_NTC1) == GPIO.LOW:

            counter = (counter + 1) % 10

    return counter

pfad.open("a", encoding="utf-8")

try:

    while len(pfad.read_text(encoding="utf-8")) // 240 < KeySets:

        if sensor == 0:
            wert = LDR1()

        if sensor == 1:
            wert = LDR2()

        if sensor == 2:
            wert = NTC1()

        speicher = speicher + str(wert)

        if len(speicher) == 2:

            wert = speicher # abc[int(speicher)] 

            with pfad.open("a", encoding="utf-8") as f:

                f.write(wert)

            with pfad.open("r", encoding="utf-8") as f:

                länge = len(f.read())

                print("Zeichen:", wert, "| KeySets:", länge // 240,"/", KeySets, "|", länge % 240, "/ 240", "|", länge, "/", KeySets*240)

            speicher = ""

        sensor = (sensor + 1) % 3

        #print(sensor)

    print("Fertig!", KeySets, "KeySets,", KeySets*240, "Zeichen, wurden generiert!")
    print(name)
    GPIO.cleanup()

    time.sleep(intervall)

except KeyboardInterrupt:
    print("\nProgramm beendet")
    GPIO.cleanup()