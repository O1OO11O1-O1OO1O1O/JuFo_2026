import RPi.GPIO as GPIO
from pathlib import Path
import time

GPIO.setmode(GPIO.BCM)
pfad = Path("/home/marten/Test Schlüssel") / "zahlen.txt" # Path("/media/marten/INTENSO") / "zahlen.txt"
abc = ["A", "Ä", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "Ö", "P", "Q", "R", "S", "T", "U", "Ü", "V", "W", "X", "Y", "Z", "a", "ä", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "ö", "p", "q", "r", "s", "t", "u", "ü", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " ", "°"]

speicher = ""
sensor = 1

KeySets = 100 #Einstellen!!!
intervall = 0.05

print("Dauer: ca.", KeySets * 240 / ((1 / intervall ) * 60), "Minuten")

PIN_LDR1 = 17  

PIN_LDR2 = 27

PIN_NTC1 = 22


def LDR1():
    GPIO.setup(PIN_LDR1, GPIO.OUT)
    GPIO.output(PIN_LDR1, GPIO.LOW)
    time.sleep(0.05)

    GPIO.setup(PIN_LDR1, GPIO.IN)
    start_time = time.time()

    while GPIO.input(PIN_LDR1) == GPIO.LOW:
        pass

    return time.time() - start_time

def LDR2():
    GPIO.setup(PIN_LDR2, GPIO.OUT)
    GPIO.output(PIN_LDR2, GPIO.LOW)
    time.sleep(0.05)

    GPIO.setup(PIN_LDR2, GPIO.IN)
    start_time = time.time()

    while GPIO.input(PIN_LDR2) == GPIO.LOW:
        pass

    return time.time() - start_time

def NTC1():
    GPIO.setup(PIN_NTC1, GPIO.OUT)
    GPIO.output(PIN_NTC1, GPIO.LOW)
    time.sleep(0.05)

    GPIO.setup(PIN_NTC1, GPIO.IN)
    start_time = time.time()

    while GPIO.input(PIN_NTC1) == GPIO.LOW:
        pass

    return time.time() - start_time


try:

    while True:

        done = False

        if sensor == 1:
            wert = str(LDR1())[-1]

        if sensor == 2:
            wert = str(LDR2())[-1]

        if sensor == 3:
            wert = str(NTC1())[-1]


        speicher = speicher + wert
        

        if len(speicher) == 2:

            wert = speicher # abc[int(speicher)] 
            

            with pfad.open("a", encoding="utf-8") as f:

                f.write(wert)

            with pfad.open("r", encoding="utf-8") as f:

                länge = len(f.read())

                if länge // 240 == KeySets:
                    done = True

                print("Zeichen:", wert, "| KeySets:", länge // 240,"/", KeySets, "|", länge % 240, "/ 240", "|", länge, "/", KeySets*240)

            speicher = ""

        if done:
            print("Fertig!", KeySets, "KeySets,", KeySets*240, "Zeichen, wurden generiert!")
            GPIO.cleanup()
            break

        sensor += 1


        if sensor == 4:
            sensor = 1

        time.sleep(intervall)

except KeyboardInterrupt:
    print("\nProgramm beendet")
    GPIO.cleanup()
