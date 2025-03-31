import tkinter as tk
from tkinter import filedialog, messagebox

def identify_hash(hash_input):
    hash_input = hash_input.strip()
    hash_len = len(hash_input)
    results = []

    if not hash_input:
        return ["Bitte gib einen Hash ein."]

    if not all(c in '0123456789abcdefABCDEF$*.' for c in hash_input):
        return ["Ungültiger Hash (nicht hexadezimal oder ungewöhnliches Format)"]

    if hash_len == 32:
        results.append("MD5 – Sehr verbreitet, unsicher")
        results.append("NTLM – Microsoft-Hash")
        if hash_input.isupper():
            results.append("LM Hash – Alt und leicht knackbar")

    elif hash_len == 40:
        results.append("SHA1 – Veraltet, nicht mehr sicher")

    elif hash_len == 41 and hash_input.startswith("*"):
        results.append("MySQL v4 – beginnt mit * und SHA1 intern")

    elif hash_len == 64:
        results.append("SHA-256 – Standard für viele sichere Systeme")
        results.append("SHA3-256 – Sicherer SHA3-Nachfolger")

    elif hash_len == 128:
        results.append("SHA-512 – Sehr lang, stark")
        results.append("SHA3-512 – SHA3-Version")

    elif hash_len == 60 and hash_input.startswith(("$2a$", "$2b$", "$2y$")):
        results.append("bcrypt – Sichere Passwortspeicherung")

    elif hash_len == 16:
        results.append("MySQL v3 – Ältere MySQL-Version")

    else:
        results.append("Unbekannter oder seltener Hash-Typ")

    return results


def on_identify():
    hash_val = entry.get()
    if not hash_val:
        messagebox.showinfo("Hinweis", "Bitte gib einen Hash ein oder wähle eine Datei.")
        return
    show_results(hash_val)


def on_load_file():
    file_path = filedialog.askopenfilename(
        title="Wähle eine Datei mit einem Hash",
        filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r") as f:
                first_line = f.readline().strip()
                if first_line:
                    entry.delete(0, tk.END)
                    entry.insert(0, first_line)
                    show_results(first_line)
                else:
                    messagebox.showerror("Fehler", "Die Datei ist leer.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Datei konnte nicht gelesen werden:\n{e}")


def show_results(hash_val):
    result_box.delete(0, tk.END)
    results = identify_hash(hash_val)
    for res in results:
        result_box.insert(tk.END, res)


# GUI
root = tk.Tk()
root.title("Hash Identifier")
root.geometry("500x350")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

label = tk.Label(frame, text="Gib den Hash ein oder lade eine Datei:")
label.pack()

entry = tk.Entry(frame, width=60)
entry.pack(pady=5)

button_frame = tk.Frame(frame)
button_frame.pack(pady=5)

button = tk.Button(button_frame, text="Hash erkennen", command=on_identify)
button.pack(side=tk.LEFT, padx=5)

file_button = tk.Button(button_frame, text="Datei auswählen", command=on_load_file)
file_button.pack(side=tk.LEFT, padx=5)

result_label = tk.Label(frame, text="Erkannte Hash-Typen:")
result_label.pack(pady=(10, 0))

result_box = tk.Listbox(frame, width=70, height=10)
result_box.pack(pady=5)

root.mainloop()
