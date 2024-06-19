import tkinter as tk
from tkinter import filedialog
from elaborazioni import leggi_video, leggi_frame
import os

initial_path = "./"


def gestisci_input(filename, fov_entry, lat_entry, lon_entry, root):
    if filename:
        if os.path.exists(filename):
            # Ottieni i valori dai campi di testo e convertili in interi
            fov = int(fov_entry.get())
            latitudine = int(lat_entry.get())
            longitutidine = int(lon_entry.get())
            _, file_extension = os.path.splitext(filename)
            # Controlla se l'estensione corrisponde a un'immagine o a un video
            if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                root.destroy()
                leggi_frame(filename, fov, latitudine, longitutidine)
            elif file_extension.lower() in ['.mp4', '.mov', '.avi', '.mkv']:
                root.destroy()
                leggi_video(filename, fov, latitudine, longitutidine)
            else:
                print("Il tipo del file non è riconosciuto come immagine o video.")
        else:
            print("Il percorso inserito non è valido.")
    else:
        print("Inserire un percorso valido.")


def crea_interfaccia():
    # Creazione della finestra principale
    root = tk.Tk()
    root.title("Visualizzatore immagini/video equirettangolari")

    path_label = tk.Label(root, text="Insert path")
    path_label.pack()

    # Creazione della riga di testo per inserire il percorso dell'immagine
    text_entry = tk.Entry(root)
    text_entry.insert(0, initial_path)
    text_entry.pack()

    # Creazione delle etichette per i campi di testo
    fov_label = tk.Label(root, text="FOV")
    fov_label.pack()

    # Creazione dei campi di testo per i parametri della funzione process_image
    fov_entry = tk.Entry(root, width=10)
    fov_entry.insert(0, "60")  # Imposta il valore predefinito a 60
    fov_entry.pack()

    lat_label = tk.Label(root, text="Latitudine")
    lat_label.pack()

    lat_entry = tk.Entry(root, width=10)
    lat_entry.insert(0, "80")  # Imposta il valore predefinito a 80
    lat_entry.pack()

    long_label = tk.Label(root, text="Longitudine")
    long_label.pack()

    lon_entry = tk.Entry(root, width=10)
    lon_entry.insert(0, "70")  # Imposta il valore predefinito a 70
    lon_entry.pack()

    # Creazione dei pulsanti per aprire un'immagine
    open_image_button_text = tk.Button(root, text="Open File from Path",
                                       command=lambda: gestisci_input(text_entry.get(), fov_entry, lat_entry, lon_entry,
                                                                      root))
    open_image_button_text.pack()

    open_image_button_dialog = tk.Button(root, text="Open File from Dialog", command=lambda:
    gestisci_input(filedialog.askopenfilename(initialdir=initial_path, title="Select File",
                                              filetypes=(("Image files", "*.jpg *.jpeg *.png *.gif"),
                                                         ("Video files", "*.mp4 *.mov *.avi *.mkv"),
                                                         ("All files", "*.*"))), fov_entry, lat_entry, lon_entry, root))
    open_image_button_dialog.pack()

    istr_label = tk.Label(root, text="Istruzioni: \n"
                                     "W = muovi alto, S = muovi basso\n "
                                     "A = muovi sinistra, D = muovi destra \n"
                                     "Q = aumenta fov , E = diminuisci fov\n"
                                     "X = aumenta zoom , Z = diminuisci zoom\n"
                                     "P = screenshot\n"
                                     "\u2423 = pausa/riproduci")
    istr_label.pack()
    # Eseguire il loop principale
    center_window(root, 500, 400)
    root.mainloop()


def center_window(window, width, height):
    # Ottieni le dimensioni dello schermo
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcola le coordinate x e y per posizionare la finestra al centro
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Imposta le coordinate della finestra
    window.geometry(f'{width}x{height}+{x}+{y}')