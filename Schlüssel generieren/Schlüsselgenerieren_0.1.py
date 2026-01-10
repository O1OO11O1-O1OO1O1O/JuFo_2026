import RPi.GPIO as GPIO
from pathlib import Path
import time

GPIO.setmode(GPIO.BCM)
pfad = Path("/media/marten/INTENSO") / "zahlen.txt"


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
        wert = str(LDR1())[-1]
        print(wert)
        with pfad.open("a", encoding="utf-8") as f:
            f.write(wert)

        wert = str(LDR2())[-1]
        print(wert)
        with pfad.open("a", encoding="utf-8") as f:
            f.write(wert)

        wert = str(NTC1())[-1]
        print(wert)
        with pfad.open("a", encoding="utf-8") as f:
            f.write(wert)
            
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nProgramm beendet")
    GPIO.cleanup()
