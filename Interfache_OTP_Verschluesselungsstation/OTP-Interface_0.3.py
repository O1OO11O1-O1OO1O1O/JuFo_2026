import tkinter as tk
import cv2
from tkinter import ttk
from PIL import Image, ImageTk #QR Code anzeigen
from tkinter import messagebox
import qrcode
from pathlib import Path
import shutil
from pyzbar.pyzbar import decode
from picamera2 import Picamera2


abc = ["A", "Ä", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "Ö", "P", "Q", "R", "S", "T", "U", "Ü", "V", "W", "X", "Y", "Z", "a", "ä", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "ö", "p", "q", "r", "s", "t", "u", "ü", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " ", "°"]
eingabeschlüssel = [] 
changer = 0
verschluesselterSatz = []
data = ""

usb = Path("/media/marten/INTENSO/zahlen.txt")
schlüssel = Path.home() / "Schlüssel" / "zahlen.txt"


root = tk.Tk()
root.title(":) 🐍 ")
root.geometry("1920x1080")
root.configure(bg="#d3d3d3")
root.attributes("-fullscreen", True)

picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
)


def QRgen(inhalt):
    
    QR_Code = tk.Toplevel(root)
    QR_Code.title("QR-Code")

    img = qrcode.make(inhalt)

    
    QR_Code.qr_img = ImageTk.PhotoImage(img)

    label = tk.Label(QR_Code, image=QR_Code.qr_img)
    label.pack(padx=10, pady=10)

def Scannen():

    picam2.start()

    qr = False
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        codes = decode(gray)

        for code in codes:
            data = code.data.decode("utf-8")
            x, y, w, h = code.rect

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
            cv2.putText(
                frame, data, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 255, 0), 2
            )
            print("QR-Code gefunden:", data)
            textfeld.delete("1.0", tk.END)
            textfeld.insert(tk.END, data)
            qr = True

        if qr:
            break

        cv2.imshow("QR Scanner (esc zum schließen)", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    picam2.stop()

def Anzeigen():

    textfeld.delete("1.0", tk.END)
    textfeld.insert(tk.END, "".join(verschluesselterSatz))

    messagebox.showinfo('Ergebniss', f'der Text wurde Ver/Entschlüsselt: {"".join(verschluesselterSatz)}')

    if changer == 1:
        QRgen("".join(verschluesselterSatz))

def Verschlüsseln():

    global changer 
    changer = 1

    RechnungOTP()

def Entschlüsseln():

    global changer
    changer = -1

    RechnungOTP()

def RechnungOTP():
    global changer
    global verschluesselterSatz
    global eingabeschlüssel

    falscheZeichen = []
    endschlüssel = []
    verschluesselterSatz = []

    Schlüsselholen()
    text_inhalt = textfeld.get("1.0", "end-1c")

    # Informationen sammeln
    

    print("text_inhalt: ", text_inhalt)
    print("eingabeschlüssel: ", eingabeschlüssel)

    for x in range(240 - len(text_inhalt)):

        text_inhalt = text_inhalt + eingabeschlüssel[x]

        #print("x: ", x)

        #print("eingabeschlüssel[x]: ", eingabeschlüssel[x])

        #print("textinhalt: ", text_inhalt)

    print("text_inhalt: ", text_inhalt)

    print(text_inhalt)

    #text an die vorgegebene Länge (240) Zeichen anpassen


    for scan in range(0,len(text_inhalt)):

        if not text_inhalt[scan] in abc:
            falscheZeichen.append(text_inhalt[scan])
    
        if not eingabeschlüssel[scan] in abc:
            falscheZeichen.append(eingabeschlüssel[scan]) 
        
    if len(falscheZeichen) > 0:
        print("Fehler:")
        print(len(falscheZeichen), "nicht unterstützte Zeichen wurden benutzt:")
        print(" ".join(falscheZeichen))

        messagebox.showerror('Fehler',str(len(falscheZeichen)) + ' nicht unterstützte Zeichen\n' + " ".join(falscheZeichen))

    #auf falsche Zeichen überprüfen


    else:

        print("len text_inhalt = ", len(text_inhalt))
        print("text_inhalt = ", text_inhalt)
        print("##########################")

        for durchlauf in range(0,len(text_inhalt)):

            print("satz: ", text_inhalt)
            print("Index: ", durchlauf +1)
        
            input = text_inhalt[durchlauf]
            print("input: ", input, abc.index(input))
            input = abc.index(input)

            Schlüssel = eingabeschlüssel[durchlauf]
            print("Schlüssel: ", Schlüssel, abc.index(Schlüssel))
            Schlüssel = abc.index(Schlüssel)
        
            verschluesselterSatz.append(abc[(input + (Schlüssel*changer))% len(abc)])
            print(input, "+", Schlüssel*changer, "mod", len(abc), "=", abc[(input + (Schlüssel*changer))% len(abc)])
            endschlüssel.append(abc[Schlüssel])
            print("Ergebnis der Berechnung", abc[(input + (Schlüssel*changer))% len(abc)])
            print(verschluesselterSatz)
            print("##########################")

        print(text_inhalt, " wurde mit ", "".join(endschlüssel), "zu", "".join(verschluesselterSatz), "ver/entschlüsselt")
        Anzeigen()

    #Ver/Entschlüsseln
´

def Schlüsselholen():

    global usb
    global schlüssel
    global eingabeschlüssel

    Schlüsselspeicherneu = []
    inhalt = schlüssel.read_text(encoding="utf-8")
    GesSchlüsselspeicher = inhalt
    eingabeschlüssel = GesSchlüsselspeicher[:240] #240 +3 *len(WalzenLager)
    Schlüsselspeicherneu = GesSchlüsselspeicher[240:]
    #schlüssel.write_text(Schlüsselspeicherneu, encoding="utf-8")

def Loeschen():
    textfeld.delete("1.0", tk.END)

def Einstellungen():
    global usb
    global schlüssel

    KeySets = len(schlüssel.read_text(encoding="utf-8")) // 240
    
    Einstellungen = tk.Toplevel(root)
    Einstellungen.transient(root)
    Einstellungen.grab_set()        
    Einstellungen.focus_force() 
    Einstellungen.title("Eistellungen")
    Einstellungen.geometry("500x400")

    überschrifft_Schlüsselspeicher = tk.Label(
        Einstellungen,
        text="Schlüsselspeicher",
        font=("Arial", 25, "bold"),
        bg="#a9a9a9",
        fg="black",
        relief="solid",
        bd=5,
    )
    überschrifft_Schlüsselspeicher.pack(pady=10)

    Button_schließen = tk.Button(
        Einstellungen,
        text="X",
        font=("Arial", 10),
        bg="#ff0000",
        fg="#000000",
        relief="solid",
        bd=5,
        command=Einstellungen.destroy
    )
    Button_schließen.place(x = 440,y = 10)

    überschrifft_KeySets = tk.Label(
        Einstellungen,
        text="KeySets:",
        font=("Arial", 18, "bold"),
        #bg="#a9a9a9",
        fg="black",
        #relief="solid",
        #bd=5,
    )
    überschrifft_KeySets.place(x = 155,y = 125)

    KeySets = tk.Label(
        Einstellungen,
        text=("-",KeySets,"-"),
        font=("Arial", 15, "bold"),
        bg="#a9a9a9",
        fg="black",
        relief="solid",
        bd=2,
    )
    KeySets.place(x = 265,y = 125)

    def SchlüsselUpdate():
        global usb
        global schlüssel

        if usb.exists():
            print("USB-Stick ist angeschlossen, Schlüsselspeicher wird Aktualisiert")
            messagebox.showinfo('SB-Stick angeschlossen', 'Schlüsselspeicher wird Aktualisiert')
            quelle = usb
            ziel = schlüssel
            ziel.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(str(quelle), str(ziel))

        else:
            print("USB-Stick nicht vorhanden")
            messagebox.showerror('SB-Stick nicht gefunden','404\n' 'Der gesuchte Pfad existiert nicht\n' )
        

    Button_update = tk.Button(
        Einstellungen,
        text=" Update ",
        font=("Arial", 15),
        bg="#a9a9a9",
        fg="black",
        relief="solid",
        bd=2,
        command=lambda: (SchlüsselUpdate(), Einstellungen.destroy())
    )
    Button_update.place(x = 200,y = 75) #y = 120

    überschrifft_SD = tk.Label(
        Einstellungen,
        text="Pfad SD Karte",
        font=("Arial", 15, "bold"),
        #bg="#a9a9a9",
        fg="black",
        #relief="solid",
        #bd=5,
    )
    überschrifft_SD.place(x = 167,y = 170) #y = 112

    textfeld_SD = tk.Text(
    Einstellungen,
    font=("Arial", 15),
    fg="black", #ff0000
    relief="solid",
    bd=2,
    wrap="word"
    )
    textfeld_SD.place(x=20, y=205, width=460, height=34)

    textfeld_SD.insert(tk.END, usb)

    überschrifft_Pfad_Schlüsselspeicher = tk.Label(
        Einstellungen,
        text="Pfad Schlüsselspeicher",
        font=("Arial", 15, "bold"),
        #bg="#a9a9a9",
        fg="black",
        #relief="solid",
        #bd=5,
    )
    überschrifft_Pfad_Schlüsselspeicher.place(x = 140,y = 250) #y = 112

    textfeld_Pfad_Schlüsselspeicher = tk.Text(
    Einstellungen,
    font=("Arial", 15),
    fg="black", #ff0000
    relief="solid",
    bd=2,
    wrap="word"
    )
    textfeld_Pfad_Schlüsselspeicher.place(x=20, y=285, width=460, height=34)

    textfeld_Pfad_Schlüsselspeicher.insert(tk.END, schlüssel)

    def Speichern():
        usb = Path(textfeld_SD.get("1.0", "end-1c"))
        schlüssel = Path(textfeld_Pfad_Schlüsselspeicher.get("1.0", "end-1c"))

    speichern = tk.Button(
        Einstellungen,
        text=" Speichern ",
        font=("Arial", 15),
        bg="#a9a9a9",
        fg="black",
        relief="solid",
        bd=2,
        command=lambda: (Speichern(), Einstellungen.destroy())
    )
    speichern.place(x = 200,y = 330) #y = 120

def limit_text(event):
    text_inhalt = textfeld.get("1.0", "end-1c")
    if len(text_inhalt) > 240:
        textfeld.delete("1.0", "end")
        textfeld.insert("1.0", text_inhalt[:240])


Überschrift = tk.Label(
    root,
    text="Verschlüsselungsstation",
    font=("Arial", 60, "bold"),
    bg="#a9a9a9",
    fg="black",
    relief="solid",
    bd=10,
    padx=20,
    pady=10
)
Überschrift.pack(anchor="w", pady=(10, 20), padx=10)

button_Loeschen = tk.Button(
    root,
    text="Löschen",
    font=("Arial", 40),
    bg="#a9a9a9",
    fg="#9370db",
    relief="solid",
    bd=10,
    command=Loeschen
)
button_Loeschen.place(x=210, y=470, width=350, height=110)

button_Einstellungen = tk.Button(
    root,
    text="Einstellungen",
    font=("Arial", 20),
    bg="#a9a9a9",
    fg="#9370db",
    relief="solid",
    bd=10,
    command=Einstellungen
)
button_Einstellungen.place(x=1750, y=20, width=100, height=100)

button_Verschlüsseln = tk.Button(
    root,
    text="Verschlüsseln",
    font=("Arial", 40),
    bg="#a9a9a9",
    fg="#9370db",
    relief="solid",
    bd=10,
    command=Verschlüsseln
)
button_Verschlüsseln.place(x=590, y=500, width=350, height=80)

button_Entschlüsseln = tk.Button(
    root,
    text="Entschlüsseln",
    font=("Arial", 40),
    bg="#a9a9a9",
    fg="#9370db",
    relief="solid",
    bd=10,
    command=Entschlüsseln
)
button_Entschlüsseln.place(x=980, y=500, width=350, height=80)

button_Kamera = tk.Button(
    root,
    text="Kamera",
    font=("Arial", 40),
    bg="#a9a9a9",
    fg="#9370db",
    relief="solid",
    bd=10,
    command=Scannen
)
button_Kamera.place(x=1360, y=470, width=350, height=110)

textfeld = tk.Text(
    root,
    font=("Arial", 40),
    fg="#9370db", #ff0000
    relief="solid",
    bd=10,
    wrap="word"
)
textfeld.place(x=210, y=600, width=1500, height=300)


textfeld.bind("<KeyRelease>", limit_text)

root.mainloop()
