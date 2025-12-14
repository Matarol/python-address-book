import tkinter as tk
from tkinter import messagebox
import csv
import os
import socket

"""
En adressboks-applikation där man kan lägga till, söka efter och uppdatera, ta bort kontakter. Det går även att skicka en
kontakt via socket.
"""

# Annotera variabler
contacts: list[dict[str]] # Innehåller kontakter som antingen läggs till eller tas bort
var_message: str = ""

# Funktion för att läsa in nuvarande data ifrån CSV-fil 
# till en lista innehållande ett dictionary för respektive contact

def read_from_csv() -> list[dict[str]]:
    content: list[dict[str]] = []
    with open("family.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            content.append(row)
    f.close()
    return content

# Funktion för att skriva till CSV-fil, antingen en befintlig eller
# så skapar den en ny. Lägger till sist i listan av kontakter i variabeln 'contacts'

def write_to_csv() -> None:
    fieldnames: list[str] = ["Förnamn", "Efternamn", "Gatunamn"]
    if not os.path.isfile("family.csv"):
        with open("family.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for row in contacts:
                writer.writeheader()
                writer.writerow(row)
    else:
        with open("family.csv", "a", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)        
            for row in contacts:
                writer.writerow(row)
    f.close()

# Funktion som kriver över befintlig CSV-fil med data som finns i variabel 'contacts'
# Används när kontakter skall raderas ur CSV-fil istället för att ta bort en specifik rad i CSV-filen.

def remove_from_csv() -> None:
    fieldnames: list[str] = ["Förnamn", "Efternamn", "Gatunamn"]
    with open("family.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in contacts:
            writer.writerow(row)

# Funktion som lagrar inmatad data i variabel 'contacts' och kör sedan 
# funktionen 'write_to_csv' som då lägger till dessa. Den kollar också om det finns
# en CSV-fil för att då kolla ifall kontakten redan finns registrerad. 
def add_contacts() -> None:
    global contacts
    global var_message
    if not os.path.isfile("family.csv"):
        if fnameEntry.get():
            add_person: list[dict[str]] = [{"Förnamn": fnameEntry.get(), "Efternamn": lnameEntry.get(), "Gatunamn": streetEntry.get()}]
            contacts = add_person
            fnameEntry.delete(0, tk.END)
            lnameEntry.delete(0, tk.END)
            streetEntry.delete(0, tk.END)
            write_to_csv()
        else:
            var_message = "Du måste ange ett förnamn och efternamn"
            messagebox.showwarning("Fel!", var_message)
    elif os.path.isfile("family.csv"):
        if fnameEntry.get():
            csv_content = read_from_csv()
            for line in csv_content:
                if fnameEntry.get() == line["Förnamn"] and lnameEntry.get() == line["Efternamn"]:
                    var_message = f"Personen med förnamn: {fnameEntry.get()} finns redan registrerad"
                    messagebox.showinfo("Information", var_message)
                    return
            add_person: list[dict[str]] = [{"Förnamn": fnameEntry.get(), "Efternamn": lnameEntry.get(), "Gatunamn": streetEntry.get()}]
            contacts = add_person
            fnameEntry.delete(0, tk.END)
            lnameEntry.delete(0, tk.END)
            streetEntry.delete(0, tk.END)
            write_to_csv()
        else:
            var_message = "Du måste ange ett förnamn och efternamn"
            messagebox.showwarning("Fel!", var_message)

# Funktion för att söka efter en kontakt och populerar resultatet i textboxen.

def find_contact() -> str:
    text_list.delete(0, tk.END)
    current_contacts = read_from_csv()
    if fnameEntry.get() == "" and lnameEntry.get() == "" and streetEntry.get() == "":
        for line in current_contacts:
            all_contacts = f"Förnamn: {line['Förnamn']} Efternamn: {line['Efternamn']} Gatunamn : {line['Gatunamn']}"
            text_list.insert(tk.END, all_contacts)
    else:
        for line in current_contacts:
            if fnameEntry.get().lower() == line["Förnamn"].lower():
                contact_match = f"Förnamn: {line['Förnamn']} Efternamn: {line['Efternamn']} Gatunamn : {line['Gatunamn']}"
                text_list.insert(tk.END, contact_match)
            elif lnameEntry.get().lower() == line["Efternamn"].lower():
                contact_match = f"Förnamn: {line['Förnamn']} Efternamn: {line['Efternamn']} Gatunamn : {line['Gatunamn']}"
                text_list.insert(tk.END, contact_match)
            elif streetEntry.get().lower() == line["Gatunamn"].lower():
                contact_match = f"Förnamn: {line['Förnamn']} Efternamn: {line['Efternamn']} Gatunamn : {line['Gatunamn']}"
                text_list.insert(tk.END, contact_match)
        fnameEntry.delete(0, tk.END)
        lnameEntry.delete(0, tk.END)
        streetEntry.delete(0, tk.END)

# Funktion för att radera kontakt. Hämtar den selekterade kontakten i textboxen (som populerats via sök-funktionen). Den läser in
# nuvarande kontakter ifrån csv-fil, itererar igenom, skapar en ny lista (names) men lägger då inte till kontakt som skall tas bort.
# Därefter körs remove_from_csv som skriver över befintlig fil med detta data. 
def delete_contact() -> None:
    global contacts
    names_list: list[dict[str]] = []
    if not text_list.get(0, tk.END):
        if text_list.get(tk.ANCHOR) == "":
            var_message = "Ingen kontkat vald för radering"
            messagebox.showwarning("Fel!", var_message)
            return
    else:
        x = text_list.get(tk.ANCHOR)
        x = x.split()
        current_contacts = read_from_csv()
        for line in current_contacts:
            if not (x[1] == line["Förnamn"] and x[3] == line["Efternamn"]):
                names_list.append(line)
        contacts = names_list
        remove_from_csv()
        text_list.delete(tk.ANCHOR)

# Funktion som tömmer textboxen via knappen 'Rensa'
def clear_text_list() -> None:
    text_list.delete(0, tk.END)

# Funktion som svarar på knapptryck 'Uppdatera' och skapar ett nytt 'toplevel'-fönster.
def open_update_contact() -> None:
    global update_window

    # Funktion som sparar uppdaterade kontakten samt tar bort den gamla
    def update_contact() -> None:
        global contacts
        names = []
        current_contacts = read_from_csv()
        updated_contact: list[dict[str]] = [{"Förnamn": fnameEntry2.get(), "Efternamn": lnameEntry2.get(), "Gatunamn": streetEntry2.get()}]
        contacts = updated_contact
        for line in current_contacts:
            if line == updated_contact[0]:
                close_update_window()
                var_message = "Inga ändringar genomfördes"
                messagebox.showinfo("Information", var_message)
                return
        write_to_csv()
        current_contacts = read_from_csv()
        contacts = names_list
        for line in current_contacts:
            if not ((names_list[0]["Förnamn"] == line["Förnamn"] or line["Förnamn"] == "") and (names_list[0]["Efternamn"] == line["Efternamn"] or line["Efternamn"] == "") and names_list[0]["Gatunamn"] == line["Gatunamn"]):
                names.append(line)
        contacts = names
        remove_from_csv()
        close_update_window()

    # Funktion som stänger update_window
    def close_update_window():
        update_window.destroy()

    if not text_list.get(0) == "":
        if not text_list.get(tk.ANCHOR) == "":
            global contacts
            names_list: list[dict[str]] = []
            contact = text_list.get(tk.ANCHOR)
            contact = contact.split()
            current_contacts = read_from_csv()
            for line in current_contacts:
                if (contact[1] == line["Förnamn"] and contact[3] == line["Efternamn"]):
                    names_list.append(line)
            
            contacts = names_list

            update_window = tk.Toplevel()
            update_window.geometry("415x300")
            update_window.title("My Gr8 Address Book - Update Contact")

            frame1 = tk.Frame(update_window)
            frame1.grid(row=0, column=0)

            fnameLabel2 = tk.Label(frame1, text="Förnamn: ", font=("comic", 15))
            fnameLabel2.grid(row=0, column=0, padx=20, pady=10)
            fnameVar = tk.StringVar(value=str(names_list[0]["Förnamn"]))
            fnameEntry2 = tk.Entry(frame1, textvariable=fnameVar, font=("comic", 15))
            fnameEntry2.grid(row=0, column=1, padx=20, pady=10)

            lnameLabel2 = tk.Label(frame1, text="Efternamn: ", font=("comic", 15))
            lnameLabel2.grid(row=1, column=0, padx=20, pady=10)
            var = tk.StringVar(value=str(names_list[0]["Efternamn"]))
            lnameEntry2 = tk.Entry(frame1, textvariable=var, font=("comic", 15))
            lnameEntry2.grid(row=1, column=1, padx=20, pady=10)

            streetLabel2 = tk.Label(frame1, text="Gatunamn: ", font=("comic", 15))
            streetLabel2.grid(row=2, column=0, padx=20, pady=10)
            var = tk.StringVar(value=str(names_list[0]["Gatunamn"]))
            streetEntry2 = tk.Entry(frame1, textvariable=var, font=("comic", 15))
            streetEntry2.grid(row=2, column=1, padx=20, pady=10)

            saveBtn = tk.Button(frame1, text="Spara", font=("comic", 10), command=update_contact)
            saveBtn.grid(row=3, column=0, padx=20, pady=10)

            cancelBtn = tk.Button(frame1, text="Stäng", font=("comic", 10), command="")
            cancelBtn.grid(row=3, column=1, padx=20, pady=10)

        else:
            var_message = "Du måste välja en kontakt att uppdatera!"
            messagebox.showwarning("Fel!", var_message)


    else:
        var_message = "Du måste välja en kontakt att uppdatera!"
        messagebox.showwarning("Fel!", var_message)

# Funktion för att skicka vald kontakt via socket till lystnande server (server.py). 
def send_contact() -> None:
    HEADER: int = 64
    PORT: int = 5050
    FORMAT: str = 'utf-8'
    DISCONNECT_MESSAGE: str = "!DISCONNECT"
    SERVER: str =  socket.gethostbyname(socket.gethostname())
    ADDR: tuple = (SERVER, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    def send(msg) -> bytes:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))

    message: str = str(text_list.get(tk.ANCHOR))

    send(message)
    send(DISCONNECT_MESSAGE)

    
# creates a Window object from the Tk class
window = tk.Tk()
window.geometry("415x450")
window.title("My Gr8 Address Book")

frame1 = tk.Frame(window)
frame1.grid(row=0, column=0)

frame2 = tk.Frame(window)
frame2.grid(row=1, column=0)

fnameLabel = tk.Label(frame1, text="Förnamn: ", font=("comic", 15))
fnameLabel.grid(row=0, column=0, columnspan=1, padx=20, pady=10)
fnameEntry = tk.Entry(frame1, font=("comic", 15))
fnameEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=10)

lnameLabel = tk.Label(frame1, text="Efternamn: ", font=("comic", 15))
lnameLabel.grid(row=1, column=0, columnspan=1, padx=20, pady=10)
lnameEntry = tk.Entry(frame1, font=("comic", 15))
lnameEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=10)

streetLabel = tk.Label(frame1, text="Gatunamn: ", font=("comic", 15))
streetLabel.grid(row=2, column=0, columnspan=1, padx=20, pady=10)
streetEntry = tk.Entry(frame1, font=("comic", 15))
streetEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=10)

submitBtn = tk.Button(frame2, text="Lägg till", font=("comic", 10), command=add_contacts)
submitBtn.grid(row=0, column=0, padx=30, pady=10)

findBtn = tk.Button(frame2, text="Sök", font=("comic", 10), command=find_contact)
findBtn.grid(row=0, column=1, padx=30, pady=10)

sendBtn = tk.Button(frame2, text="Skicka", font=("comic", 10), command=send_contact)
sendBtn.grid(row=0, column=2, padx=30, pady=10)

text_list = tk.Listbox(frame2)
text_list.grid(row=1, column=0, columnspan=4, sticky="ew", pady=10)

updateBtn = tk.Button(frame2, text="Uppdatera", font=("comic", 10), command=open_update_contact)
updateBtn.grid(row=2, column=0, padx=30, pady=10)

deleteBtn = tk.Button(frame2, text="Radera", font=("comic", 10), command=delete_contact)
deleteBtn.grid(row=2, column=1, padx=30, pady=10)

clearBtn = tk.Button(frame2, text="Rensa", font=("comic", 10), command=clear_text_list)
clearBtn.grid(row=2, column=2, padx=30, pady=10)

window.mainloop()
