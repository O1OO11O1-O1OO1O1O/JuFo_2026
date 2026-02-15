from pathlib import Path
from PIL import Image
import math

name = "zahlen0.005" + ".txt"

pfad = Path(r"C:\Users\nn\Documents\Rand") / name

index2 = 0

Zeichen = {}

with pfad.open("r", encoding="utf-8") as f:

    länge = len(f.read())



width, height = math.ceil(math.sqrt(länge)), math.ceil(math.sqrt(länge))
img = Image.new("RGB", (width, height), (255, 0, 0))



pixels = img.load()


#pixels[10, 10] = (255, 0, 0)   # Rot
#pixels[20, 20] = (0, 255, 0)   # Grün
#pixels[30, 30] = (0, 0, 255)   # Blau

with pfad.open("r", encoding="utf-8") as f:
    input = f.read()


for zeile in range(math.ceil(math.sqrt(länge))):

    for index in range(math.ceil(math.sqrt(länge))):

        pixels[index, zeile] = (int(int(input[index2]) * (25.5)), int(int(input[index2]) * (25.5)), int(int(input[index2]) * (25.5)))   # Rot
        
        if input[index2] in Zeichen:
            Zeichen[input[index2]] += 1

        else:
            Zeichen[input[index2]] = 1


        if index2 < len(input) -1:
            index2 += 1

        else:
            break

nameimg = "img_" + name + "_.png"

img.save(nameimg)

print("Bild gespeichert:", nameimg)

for zeichen, anzahl in Zeichen.items():
    print(f" '{zeichen}' : {anzahl} mal", round(100 / länge * anzahl, 2), "%")

    balken = ""

    for x in range(round(100 / länge * anzahl)):
        balken = balken + "#"

    print("B:", balken)
    print()


print("Gesamt:", länge, "Zeichen")
print("B: ####################################################################################################")
print()

#for x in range(100):
#    balken = balken + "#"
#print("B:", balken)

print(Zeichen)
