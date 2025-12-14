import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import csv


# Klass som hanterar all läsning/skrivning av data (kontaktinformation) till csv-fil.
class Model:
    def __init__(self):
        pass
    
    # Metod som sparar kontaktinfo i:
    # - en ny fil om ingen fil redan finns
    # - sist i en befintlig fil ifall kontakt inte redan finns registrerad 
    def save(self):
        fieldnames: list[str] = ["Förnamn", "Efternamn", "Gatunamn"]
        if not os.path.isfile("kontakter.csv"):
            with open("kontakter.csv", "w", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(self.input)
        else:
            exists = self.check_if_contact_exist()
            if not exists:
                with open("kontakter.csv", "a", newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)        
                    writer.writerow(self.input)
                f.close()

    # Metod som kollar ifall kontakt redan finns registrad (returnerar i så fall True)
    # eller inte (returnerar i så fall False)
    def check_if_contact_exist(self) -> bool:
        current_contacts: list[dict[str]]
        current_contacts = self.read_currentContacts_from_csv()
        for row in current_contacts:
            if (row["Förnamn"] == self.input["Förnamn"] and row["Efternamn"] == self.input["Efternamn"]):
                messagebox.showinfo(title="Information", message=f"Kontakt med namn: {self.input["Förnamn"]} {self.input["Efternamn"]} finns redan i addressbok!")
                return True
                
        return False          

    # Metod som läser in alla befintliga kontakter till en lista som också returneras
    def read_currentContacts_from_csv(self):

        current_contacts: list[dict[str]] = []
        with open("kontakter.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                current_contacts.append(row)
        return current_contacts

    def search(self) -> list[dict[str]]:
        search_result: list[str] = []
        current_contacts = self.read_currentContacts_from_csv()
        input_key = list(self.input.keys())
        if len(list(self.input.keys())) == 1:
            for row in current_contacts:
                if row[input_key[0]] == self.input[str(input_key[0])]:
                    search_result.append(row)
                    # print(f"Träff på {row[input_key[0]]} som är samma som {self.input[str(input_key[0])]}")
        elif len(list(self.input.keys())) == 2:
            for row in current_contacts:
                if (row[input_key[0]] == self.input[str(input_key[0])] and row[input_key[1]] == self.input[str(input_key[1])]):
                    search_result.append(row)
                    # print(f"Träff på {row[input_key[0]]} och {row[input_key[1]]} som är samma som {self.input[str(input_key[0])]} och {row[input_key[1]]}")
        else:
            for row in current_contacts:
                if (row[input_key[0]] == self.input[str(input_key[0])] and row[input_key[1]] == self.input[str(input_key[1])] and row[input_key[2]] == self.input[str(input_key[2])]):
                    search_result.append(row)
                    # print(f"Träff på {row[input_key[0]]}, {row[input_key[1]]} och {row[input_key[2]]} som är samma som {self.input[str(input_key[0])]}, {row[input_key[1]]} och {row[input_key[2]]}")
        return search_result
                        

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Skapa widgets
        # Labels
        self.fnameLabel = ttk.Label(self, text="Förnamn: ")
        self.fnameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.lnameLabel = ttk.Label(self, text="Efternamn: ")
        self.lnameLabel.grid(row=1, column=0, padx=10, pady=10)
        self.streetLabel = ttk.Label(self, text="Gatunamn: ")
        self.streetLabel.grid(row=2, column=0, padx=10, pady=10)

        # contact entrys
        self.fname_var = tk.StringVar()
        self.fnameEntry = ttk.Entry(self, textvariable=self.fname_var, width=30)
        self.fnameEntry.grid(row=0, column=1, sticky=tk.NSEW)
        self.lname_var = tk.StringVar()
        self.lnameEntry = ttk.Entry(self, textvariable=self.lname_var, width=30)
        self.lnameEntry.grid(row=1, column=1, sticky=tk.NSEW)
        self.street_var = tk.StringVar()
        self.streetEntry = ttk.Entry(self, textvariable=self.street_var, width=30)
        self.streetEntry.grid(row=2, column=1, sticky=tk.NSEW)

        # lisbox
        self.text_list = tk.Listbox(self)
        self.text_list.grid(row=4, column=0, columnspan=3, sticky='ew')

        # buttons
        self.saveBtn = ttk.Button(self, text='Lägg till', command=self.save_button_clicked)
        self.saveBtn.grid(row=3, column=0, padx=10, pady=10)
        self.searchBtn = ttk.Button(self, text='sök', command=self.search_button_clicked)
        self.searchBtn.grid(row=3, column=1, padx=10, pady=10)
        self.sendBtn = ttk.Button(self, text='Skicka', command="self.send_button_clicked")
        self.sendBtn.grid(row=3, column=2, padx=10, pady=10)
        updateBtn = ttk.Button(self, text="Uppdatera", command=self.update_button_clicked)
        updateBtn.grid(row=5, column=0, padx=10, pady=10)
        deleteBtn = ttk.Button(self, text="Radera", command="self.delete_button_clicked")
        deleteBtn.grid(row=5, column=1, padx=10, pady=10)
        clearBtn = ttk.Button(self, text="Rensa", command="self.clear_text_list")
        clearBtn.grid(row=5, column=2, padx=10, pady=10)
    

    def set_controller(self, controller):
        self.controller = controller

    def save_button_clicked(self):
        if self.fnameEntry.get() == "" or self.lnameEntry.get() == "" or self.streetEntry.get() == "":
            messagebox.showinfo("Information", "För- efter- samt gatunamn måste anges")
            return
        else:
            if self.controller:
                self.controller.save({"Förnamn": self.fname_var.get(), "Efternamn": self.lname_var.get(), "Gatunamn": self.street_var.get()})
                self.fnameEntry.delete(0, tk.END)
                self.lnameEntry.delete(0, tk.END)
                self.streetEntry.delete(0, tk.END)
    
    def search_button_clicked(self):
        search_string: dict[str] = {}
        if not self.fname_var.get():
            if not self.lname_var.get():
                search_string.update({"Gatunamn": self.street_var.get()})
                if not self.street_var.get():
                    messagebox.showinfo("Information", "Du måste ange minst ett sökriterie!")
            else:
                if not self.street_var.get():
                    search_string.update({"Efternamn": self.lname_var.get()})
                else:
                    search_string.update({"Efternamn": self.lname_var.get(), "Gatunamn": self.street_var.get()})
        else:
            if not self.lname_var.get():
                if not self.street_var.get():
                    search_string.update({"Förnamn": self.fname_var.get()})
                else:
                    search_string.update({"Förnamn": self.fname_var.get(), "Gatunamn": self.street_var.get()})
            else:
                if not self.street_var.get():
                    search_string.update({"Förnamn": self.fname_var.get(), "Efternamn": self.lname_var.get()})
                else:
                    search_string.update({"Förnamn": self.fname_var.get(), "Efternamn": self.lname_var.get(), "Gatunamn": self.street_var.get()})
        if self.controller:
            self.controller.search(search_string)
        self.fnameEntry.delete(0, tk.END)
        self.lnameEntry.delete(0, tk.END)
        self.streetEntry.delete(0, tk.END)

    def update_button_clicked(self):
        updateWindow = UpdateWindow(self.update)

    def update(self, updated_fname):
        print("Update function belonging to main window was called")
        print(updated_fname)


    def search_return(self):
        for row in range(len(self.search_result)):
            search_result = f"Förnamn: {self.search_result[row]["Förnamn"]} Efternamn: {self.search_result[row]["Efternamn"]} Gatunamn: {self.search_result[row]["Gatunamn"]}"
            self.text_list.insert(tk.END, search_result)




            

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, input):
        self.model.input = input
        self.model.save()

    def search(self, input):
        self.model.input = input
        search_result = self.model.search()
        self.view.search_result = search_result
        self.view.search_return()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Addressbok utifrån MVC tänk')

        model = Model()

        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        controller = Controller(model, view)

        view.set_controller(controller)

class UpdateWindow:
    def __init__(self, update):
        top = tk.Toplevel()
        self.frame = ttk.Frame(top)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self.update = update

        self.fname_var2 = tk.StringVar()
        fnameLabel = ttk.Label(self.frame, text="Förnamn: ", font=("comic", 15))
        fnameLabel.grid(row=0, column=0, columnspan=1, padx=20, pady=10)
        fnameEntry = ttk.Entry(self.frame, textvariable=self.fname_var2, font=("comic", 15))
        fnameEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=10)

        saveBtn = ttk.Button(self.frame, text="Spara", command=update)
        saveBtn.grid(row=3, column=0, padx=20, pady=10)

        cancelBtn = ttk.Button(self.frame, text="Stäng", command="")
        cancelBtn.grid(row=3, column=1, padx=20, pady=10)

    def save_button_clicked(self):
        self.update(self.fname_var2.get())


if __name__ == "__main__":
    app = App()
    app.mainloop()
