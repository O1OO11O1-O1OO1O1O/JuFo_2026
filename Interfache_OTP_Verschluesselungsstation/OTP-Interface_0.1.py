import tkinter as tk
import cv2
from tkinter import ttk
from PIL import Image, ImageTk #QR Code anzeigen
from tkinter import messagebox
import qrcode
from pathlib import Path
import shutil



abc = ["A", "Ä", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "Ö", "P", "Q", "R", "S", "T", "U", "Ü", "V", "W", "X", "Y", "Z", "a", "ä", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "ö", "p", "q", "r", "s", "t", "u", "ü", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", " ", "°"]
eingabeschlüssel = [] #"glkedräölkgjsäflkadfpghjksflökadöbälaskfj'SÖLkbsldknvm'ÖLYDkvcALÖdbmldasnmvcs.mDKfgnmaVMD.VBNS_lvcJASÖL'GKxö M_sMFasöBMVDÖALMSKDMNVöVMDfläöVBMS'öCMSBMDvMSvölKMDBKNSMVCMÖLDFMVsdölVCMölVBMDÖVMDÖVKBMSDldM;DÖLKVMSDÖVMMVMVMV-:S;MVölVMÖSVMS'LÖK12"
changer = 0
verschluesselterSatz = []
data = ""

root = tk.Tk()
root.title(":) 🐍 ")
root.geometry("1920x1080" \
"")
root.configure(bg="#d3d3d3") #Hintergrund Fenster
#root.attributes("-fullscreen", True)

def QRgen(inhalt):
    # Neues Zusatzfenster (KEIN Tk!)
    qr_window = tk.Toplevel(root)
    qr_window.title("QR-Code")

    img = qrcode.make(inhalt)

    # Referenz AM FENSTER speichern
    qr_window.qr_img = ImageTk.PhotoImage(img)

    label = tk.Label(qr_window, image=qr_window.qr_img)
    label.pack(padx=10, pady=10)

def Scannen():
    global cap, cam_label

    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    # Nebenfenster
    cam_window = tk.Toplevel(root)
    cam_window.title("Kamera")
    cam_window.geometry("640x480")

    cam_label = tk.Label(cam_window)
    cam_label.pack()

    def update_frame():
        if not cap.isOpened():
            return

        ret, frame = cap.read()
        if not ret:
            return

        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None:
            pts = bbox.astype(int).reshape(-1, 2)
            for i in range(len(pts)):
                cv2.line(frame,
                         tuple(pts[i]),
                         tuple(pts[(i + 1) % len(pts)]),
                         (255, 0, 255), 2)

            if data:
                cv2.putText(frame, data, (pts[0][0], pts[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                print("data found:", data)
                textfeld.delete("1.0", tk.END)
                textfeld.insert(tk.END, data)

                close_camera()
                return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        cam_label.imgtk = imgtk
        cam_label.configure(image=imgtk)

        cam_label.after(10, update_frame)

    def close_camera():
        if cap:
            cap.release()
        cam_window.destroy()

    cam_window.protocol("WM_DELETE_WINDOW", close_camera)

    update_frame()

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
    

    #print(":)")

def Schlüsselholen():

    usb = Path("/media/marten/INTENSO/zahlen.txt")
    schlüssel = Path.home() / "Schlüssel" / "zahlen.txt"

    if usb.exists():
        print("USB-Stick ist angeschlossen, Schlüsselspeicher wird Aktualisiert")
        messagebox.showinfo('SB-Stick angeschlossen', 'Schlüsselspeicher wird Aktualisiert')
        quelle = usb
        ziel = schlüssel
        ziel.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(str(quelle), str(ziel))

    else:
        print("USB-Stick nicht vorhanden")



    global eingabeschlüssel

    Schlüsselspeicherneu = []


    inhalt = schlüssel.read_text(encoding="utf-8")

    GesSchlüsselspeicher = inhalt

    eingabeschlüssel = GesSchlüsselspeicher[:240] #240 +3 *len(WalzenLager)

    Schlüsselspeicherneu = GesSchlüsselspeicher[240:]
    
    #schlüssel.write_text(Schlüsselspeicherneu, encoding="utf-8")


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

Überschrift2 = tk.Label(
    root,
    text="Dein Text",
    font=("Arial", 40, "bold"),
    bg="#a9a9a9",
    fg="black",
    relief="solid",
    bd=10,
    padx=20,
    pady=10
)
Überschrift2.place(x=210, y=470, width=350, height=110)


button_Settings = tk.Button(
    root,
    text="Settings",
    font=("Arial", 20),
    bg="#a9a9a9",
    fg="#9370db",
    relief="solid",
    bd=10
)
button_Settings.place(x=1750, y=20, width=100, height=100)

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
    fg="#9370db",
    relief="solid",
    bd=10,
    wrap="word"
)
textfeld.place(x=210, y=600, width=1500, height=300)

def limit_text(event):
    text_inhalt = textfeld.get("1.0", "end-1c")
    if len(text_inhalt) > 240:
        textfeld.delete("1.0", "end")
        textfeld.insert("1.0", text_inhalt[:240])

textfeld.bind("<KeyRelease>", limit_text)


root.mainloop()
