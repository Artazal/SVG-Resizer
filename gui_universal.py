from svg_service_universal import enlarge_multiple_svgs
from tkinter import filedialog, Label, Button, StringVar, Listbox, END, Frame, Entry, messagebox
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD

file_paths = []


def browse_files():
    global file_paths
    global message
    file_paths = filedialog.askopenfilenames(
        title="Select .SVG files",
        filetypes=[("SVG files", "*.svg")]
    )
    refresh_file_list()

def handle_drop(event):
    global file_paths

    dropped = app.tk.splitlist(event.data)

    svg_files = []
    skipped = 0
    duplicates = 0

    for path in dropped:
        path = path.strip("{}")

        if not path.lower().endswith(".svg"):
            skipped += 1
            continue

        if path in file_paths or path in svg_files:
            duplicates += 1
            continue

        svg_files.append(path)

    if not svg_files and skipped == 0 and duplicates > 0:
        if duplicates == 1:
            message.set("This file is already added")
        else:
            message.set("These files are already added")
        return

    if not svg_files and skipped > 0:
        message.set("Only .SVG files are allowed")
        return

    file_paths.extend(svg_files)
    refresh_file_list()

    parts = []

    if len(svg_files) == 1:
        parts.append(f"Added 1 file")
    else:
        parts.append(f"Added {len(svg_files)} files")
    if duplicates == 1:
        parts.append("1 duplicate ignored")
    else:
        parts.append(f"{duplicates} duplicates ignored")
    if skipped:
        parts.append(f"{skipped} non-SVG skipped")

    message.set(". ".join(parts))

def refresh_file_list():
    count = len(file_paths)
    if count == 1:
        message.set("1 file selected")
    elif count > 1:
        message.set(f"{count} files selected")
    else:
        message.set("No files selected")
    file_list.delete(0, END)
    for file in file_paths:
        name = Path(file).name
        file_list.insert(END, name)
    return file_paths

def clear_selection():
    global file_paths
    file_paths = []
    file_list.delete(0, END)
    message.set("Selection cleared")

def enlarge_selected_files():
    if not file_paths:
        message.set("Please select at least one .SVG file")
        return

    try:
        target_width = int(width_var.get())
    except ValueError:
        message.set("Enter a valid whole number")
        return

    if target_width < 1:
        message.set("Target width cannot be less than 1")
        return

    if target_width > 50000:
        message.set("Target width cannot be more than 50000")
        return

    try:
        results = enlarge_multiple_svgs(file_paths, target_width)
    except Exception as e:
        message.set("Error occurred")
        print("ERROR:", e)
        return

    file_list.delete(0, END)
    errors = []

    for file_path, status, info in results:
        name = Path(file_path).name

        if status == "OK":
            file_list.insert(END, f"{name} — OK")
            file_list.itemconfig(END, {'fg': 'green'})
        else:
            file_list.insert(END, f"{name} — ERROR")
            file_list.itemconfig(END, {'fg': 'red'})
            errors.append((name, info))

    if errors:
        error_lines = []

        for name, info in errors:
            if "viewBox" in info:
                user_error = "missing required size data"
            else:
                user_error = info

            error_lines.append(f"{name}: {user_error}")

        messagebox.showerror(
            "Some files could not be resized",
            "\n".join(error_lines),
            parent=app
        )
        message.set("Some files could not be resized")
    else:
        if len(results) == 1:
            message.set("File saved next to original")
        else:
            message.set("Files saved next to originals")
   

app = TkinterDnD.Tk()
app.title("SVG Resizer")
window_width = 450
window_height = 300
width_var = StringVar(value="7000")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x}+{y}")
message = StringVar()
message.set('Add SVG files or drag and drop them into the list below')

top_frame = Frame(app)
top_frame.pack(pady=5)

second_top_frame = Frame(app)
second_top_frame.pack(pady=5)

middle_frame = Frame(app)
middle_frame.pack(pady=5)

bottom_frame = Frame(app)
bottom_frame.pack(pady=5)

l2 = Label(top_frame, textvariable = message, height = 3)
l2.pack(side = 'top')
l3 = Label(second_top_frame, text="Target width (px):").pack(side="left")
e1 = Entry(second_top_frame, textvariable=width_var, width=8).pack(side="right")
b1 = Button(middle_frame, text = "Add SVG files", width = 10, command = browse_files)
b1.pack(side = 'left', padx = 10, pady = 10)
b3 = Button(middle_frame, text = "Clear selection", width = 10, command = clear_selection)
b3.pack(side = 'left', padx = 10, pady = 10)
b2 = Button(middle_frame, text = "Resize", width = 10, command = enlarge_selected_files)
b2.pack(side = 'right', padx = 10, pady = 10)
file_list = Listbox(bottom_frame, width=80, height=10)
file_list.pack()
file_list.drop_target_register(DND_FILES)
file_list.dnd_bind("<<Drop>>", handle_drop)
app.mainloop()