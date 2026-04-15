from tkinter import *
import os
import json
from PIL import Image, ImageTk

# This App was AI generated, so expect some weird code and no comments, I will add comments later, maybe
# This is not my Code and i dont take Creddit for it.
# I only use it for time saving and to have a better overview of the JSON data.

# ----------------------------
# Paths
# ----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "..", "JSON's", "Pals.json")
ICON_DIR = os.path.join(BASE_DIR, "..", "Icons")

# ----------------------------
# JSON handling
# ----------------------------

def load_json():
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_json():
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

data = load_json()
current_index = 0
current_image = None


# ----------------------------
# Frame switching
# ----------------------------

def show_frame(frame):
    menu_frame.pack_forget()
    dex_frame.pack_forget()
    editor_frame.pack_forget()
    frame.pack(fill="both", expand=True)


# ----------------------------
# Display Pal
# ----------------------------

def display_pal(index):
    global current_image

    pal = data["pals"][index]

    label_number.config(text=f"#{pal['paldex_number']}")
    label_name.config(text=pal["name"]["display"])
    label_id.config(text=f"ID: {pal['name']['internal_id']}")
    label_types.config(text=" / ".join(pal["types"]))
    label_desc.config(text=pal["description"])

    try:
        icon_path = os.path.join(ICON_DIR, pal["icon_path"])

        img = Image.open(icon_path)
        img = img.resize((80, 80))

        current_image = ImageTk.PhotoImage(img)
        label_icon.config(image=current_image, text="")

    except:
        label_icon.config(image="", text="No Image")


# ----------------------------
# Navigation
# ----------------------------

def next_pal():
    global current_index
    if current_index < len(data["pals"]) - 1:
        current_index += 1
        display_pal(current_index)

def prev_pal():
    global current_index
    if current_index > 0:
        current_index -= 1
        display_pal(current_index)


# ----------------------------
# Icon Preview
# ----------------------------

def preview_icon():
    global current_image

    icon_name = entry_icon.get().strip()
    if not icon_name:
        return

    icon_path = os.path.join(ICON_DIR, icon_name)

    try:
        img = Image.open(icon_path)
        img = img.resize((80, 80))

        current_image = ImageTk.PhotoImage(img)
        label_icon_preview.config(image=current_image, text="")

    except:
        label_icon_preview.config(text="Icon not found", image="")


# ----------------------------
# Editor: Load Pal
# ----------------------------

def load_selected_pal(event):
    global current_index

    selection = pal_listbox.curselection()
    if not selection:
        return

    current_index = selection[0]
    pal = data["pals"][current_index]

    entry_number.delete(0, END)
    entry_number.insert(0, pal["paldex_number"])

    entry_name.delete(0, END)
    entry_name.insert(0, pal["name"]["display"])

    entry_id.delete(0, END)
    entry_id.insert(0, pal["name"]["internal_id"])

    entry_types.delete(0, END)
    entry_types.insert(0, ", ".join(pal["types"]))

    entry_icon.delete(0, END)
    entry_icon.insert(0, pal["icon_path"])

    text_desc.delete("1.0", END)
    text_desc.insert("1.0", pal["description"])

    # Work suitability
    for key in work_entries:
        work_entries[key].delete(0, END)
        work_entries[key].insert(0, pal["work_suitability"].get(key, 0))

    # Items
    item_listbox.delete(0, END)
    for item in pal["item_drops"]:
        item_listbox.insert(END, f"{item['item_name']}|{item['drop_chance']}|{item['amount']}")


# ----------------------------
# New Pal
# ----------------------------

def new_pal():
    global current_index
    current_index = None

    entry_number.delete(0, END)
    entry_name.delete(0, END)
    entry_id.delete(0, END)
    entry_types.delete(0, END)
    entry_icon.delete(0, END)
    text_desc.delete("1.0", END)

    for key in work_entries:
        work_entries[key].delete(0, END)
        work_entries[key].insert(0, "0")

    item_listbox.delete(0, END)


# ----------------------------
# Add item
# ----------------------------

def add_item():
    name = entry_item_name.get()
    chance = entry_item_chance.get()
    amount = entry_item_amount.get()

    if name:
        item_listbox.insert(END, f"{name}|{chance}|{amount}")


# ----------------------------
# Save
# ----------------------------

def save_changes():
    global current_index

    work_data = {k: int(work_entries[k].get()) for k in work_entries}

    item_drops = []
    for i in range(item_listbox.size()):
        raw = item_listbox.get(i)
        parts = raw.split("|")
        if len(parts) == 3:
            item_drops.append({
                "item_name": parts[0],
                "drop_chance": parts[1],
                "amount": parts[2]
            })

    new_entry = {
        "paldex_number": entry_number.get(),
        "name": {
            "display": entry_name.get(),
            "internal_id": entry_id.get()
        },
        "icon_path": entry_icon.get().strip(),
        "types": [t.strip() for t in entry_types.get().split(",")],
        "description": text_desc.get("1.0", END).strip(),
        "work_suitability": work_data,
        "item_drops": item_drops
    }

    if current_index is not None:
        data["pals"][current_index] = new_entry
    else:
        data["pals"].append(new_entry)
        current_index = len(data["pals"]) - 1

    save_json()
    refresh_list()


# ----------------------------
# Refresh list
# ----------------------------

def refresh_list():
    pal_listbox.delete(0, END)
    for pal in data["pals"]:
        pal_listbox.insert(END, f"#{pal['paldex_number']} - {pal['name']['display']}")


# ----------------------------
# UI
# ----------------------------

root = Tk()
root.state("zoomed")
root.minsize(800, 600)

# MENU
menu_frame = Frame(root)
Button(menu_frame, text="Dex", command=lambda: show_frame(dex_frame)).pack()
Button(menu_frame, text="Editor", command=lambda: show_frame(editor_frame)).pack()

# DEX
dex_frame = Frame(root)

label_icon = Label(dex_frame)
label_icon.pack()

label_number = Label(dex_frame); label_number.pack()
label_name = Label(dex_frame); label_name.pack()
label_id = Label(dex_frame); label_id.pack()
label_types = Label(dex_frame); label_types.pack()
label_desc = Label(dex_frame, wraplength=400); label_desc.pack()

Button(dex_frame, text="Prev", command=prev_pal).pack()
Button(dex_frame, text="Next", command=next_pal).pack()
Button(dex_frame, text="Back", command=lambda: show_frame(menu_frame)).pack()

# EDITOR
editor_frame = Frame(root)

# LEFT LIST
pal_listbox = Listbox(editor_frame, width=30)
pal_listbox.grid(row=0, column=0, rowspan=50)
pal_listbox.bind("<<ListboxSelect>>", load_selected_pal)

Label(editor_frame, text="Number").grid(row=0, column=1, sticky="w")
entry_number = Entry(editor_frame)
entry_number.grid(row=0, column=2)

Label(editor_frame, text="Name").grid(row=1, column=1, sticky="w")
entry_name = Entry(editor_frame)
entry_name.grid(row=1, column=2)

Label(editor_frame, text="Internal ID").grid(row=2, column=1, sticky="w")
entry_id = Entry(editor_frame)
entry_id.grid(row=2, column=2)

Label(editor_frame, text="Types (comma separated)").grid(row=3, column=1, sticky="w")
entry_types = Entry(editor_frame)
entry_types.grid(row=3, column=2)

Label(editor_frame, text="Icon Filename").grid(row=4, column=1, sticky="w")
entry_icon = Entry(editor_frame)
entry_icon.grid(row=4, column=2)

Button(editor_frame, text="Preview Icon", command=preview_icon).grid(row=4, column=3)

label_icon_preview = Label(editor_frame, text="No Preview")
label_icon_preview.grid(row=5, column=3)

Label(editor_frame, text="Description").grid(row=5, column=1, sticky="nw")
text_desc = Text(editor_frame, height=5, width=30)
text_desc.grid(row=5, column=2)

'''
# FIELDS
entry_number = Entry(editor_frame); entry_number.grid(row=0, column=1)
entry_name = Entry(editor_frame); entry_name.grid(row=1, column=1)
entry_id = Entry(editor_frame); entry_id.grid(row=2, column=1)
entry_types = Entry(editor_frame); entry_types.grid(row=3, column=1)

# ICON ENTRY + PREVIEW
entry_icon = Entry(editor_frame)
entry_icon.grid(row=4, column=1)

Button(editor_frame, text="Preview Icon", command=preview_icon).grid(row=4, column=2)

label_icon_preview = Label(editor_frame, text="No Preview")
label_icon_preview.grid(row=5, column=2)

text_desc = Text(editor_frame, height=5, width=30)
text_desc.grid(row=5, column=1)
'''

# WORK SUITABILITY
work_entries = {}
row = 6

work_keys = data["pals"][0]["work_suitability"].keys()

for key in work_keys:
    Label(editor_frame, text=key.replace("_", " ").title()).grid(row=row, column=1, sticky="w")

    e = Spinbox(editor_frame, from_=0, to=5, width=5)
    e.grid(row=row, column=2)

    work_entries[key] = e
    row += 1

# ITEMS
entry_item_name = Entry(editor_frame); entry_item_name.grid(row=row, column=1)
entry_item_chance = Entry(editor_frame); entry_item_chance.grid(row=row+1, column=1)
entry_item_amount = Entry(editor_frame); entry_item_amount.grid(row=row+2, column=1)

Button(editor_frame, text="Add Item", command=add_item).grid(row=row+3, column=1)

item_listbox = Listbox(editor_frame)
item_listbox.grid(row=row+4, column=1)

# BUTTONS
Button(editor_frame, text="New", command=new_pal).grid(row=row+5, column=1)
Button(editor_frame, text="Save", command=save_changes).grid(row=row+6, column=1)
Button(editor_frame, text="Back", command=lambda: show_frame(menu_frame)).grid(row=row+7, column=1)

# START
menu_frame.pack()
refresh_list()
root.mainloop()