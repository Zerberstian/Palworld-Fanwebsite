from tkinter import *
import os
import json
from PIL import Image, ImageTk

# ============================================================
# NOTE
# This app was AI-generated and later modified.
# It is used as a JSON editor / viewer for Pal data.
# ============================================================

# ============================================================
# PATHS (file locations)
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# JSON data file (all Pal data is stored here)
JSON_PATH = os.path.join(BASE_DIR, "..", "JSON's", "Pals.json")

# Folder where all icon images are stored
ICON_DIR = os.path.join(BASE_DIR, "..", "Icons")


# ============================================================
# JSON HANDLING (load / save data)
# ============================================================

def load_json():
    """Load Pal data from JSON file"""
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json():
    """Save current data back into JSON file"""
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Load data once at startup
data = load_json()

# Keeps track of which Pal is currently selected
current_index = 0

# Needed to prevent images from being garbage collected
current_image = None


# ============================================================
# FRAME SWITCHING (menu / dex / editor)
# ============================================================

def show_frame(frame):
    """Hide all frames and show only the selected one"""
    menu_frame.pack_forget()
    dex_frame.pack_forget()
    editor_frame.pack_forget()
    frame.pack(fill="both", expand=True)


# ============================================================
# DEX DISPLAY (read-only view of Pal)
# ============================================================

def display_pal(index):
    """Display Pal information in the Dex view"""
    global current_image

    pal = data["pals"][index]

    # Basic text info
    label_number.config(text=f"#{pal['paldex_number']}")
    label_name.config(text=pal["name"]["display"])
    label_id.config(text=f"ID: {pal['name']['internal_id']}")
    label_types.config(text=" / ".join(pal["types"]))
    label_desc.config(text=pal["description"])

    # Load icon image
    try:
        icon_path = os.path.join(ICON_DIR, pal["icon_path"])

        img = Image.open(icon_path)
        img = img.resize((80, 80))

        current_image = ImageTk.PhotoImage(img)
        label_icon.config(image=current_image, text="")

    except:
        # Fallback if image is missing
        label_icon.config(image="", text="No Image")


# ============================================================
# NAVIGATION (next / previous Pal)
# ============================================================

def next_pal():
    """Go to next Pal"""
    global current_index
    if current_index < len(data["pals"]) - 1:
        current_index += 1
        display_pal(current_index)


def prev_pal():
    """Go to previous Pal"""
    global current_index
    if current_index > 0:
        current_index -= 1
        display_pal(current_index)


# ============================================================
# ICON PREVIEW (editor helper)
# ============================================================

def preview_icon():
    """Preview icon from filename entered in editor"""
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


# ============================================================
# EDITOR: LOAD SELECTED PAL INTO FIELDS
# ============================================================

def load_selected_pal(event):
    """Load selected Pal into editor fields"""

    global current_index

    selection = pal_listbox.curselection()
    if not selection:
        return

    current_index = selection[0]
    pal = data["pals"][current_index]

    # Fill basic fields
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

    # Fill work suitability spinboxes
    for key in work_entries:
        work_entries[key].delete(0, END)
        work_entries[key].insert(0, pal["work_suitability"].get(key, 0))

    # Fill item drops list
    item_listbox.delete(0, END)
    for item in pal["item_drops"]:
        item_listbox.insert(END, f"{item['item_name']}|{item['drop_chance']}|{item['amount']}")


# ============================================================
# NEW PAL (clear editor for new entry)
# ============================================================

def new_pal():
    """Reset editor for creating a new Pal"""

    global current_index
    current_index = None

    entry_number.delete(0, END)
    entry_name.delete(0, END)
    entry_id.delete(0, END)
    entry_types.delete(0, END)
    entry_icon.delete(0, END)
    text_desc.delete("1.0", END)

    # Reset all work values to 0
    for key in work_entries:
        work_entries[key].delete(0, END)
        work_entries[key].insert(0, "0")

    item_listbox.delete(0, END)


# ============================================================
# ITEM SYSTEM (add loot drops)
# ============================================================

def add_item():
    """Add item drop to listbox"""

    name = entry_item_name.get()
    chance = entry_item_chance.get()
    amount = entry_item_amount.get()

    if name:
        item_listbox.insert(END, f"{name}|{chance}|{amount}")


# ============================================================
# SAVE SYSTEM (write changes back to JSON)
# ============================================================

def save_changes():
    """Save editor data into JSON file"""

    global current_index

    # Convert spinboxes into dictionary
    work_data = {k: int(work_entries[k].get()) for k in work_entries}

    # Convert item listbox into structured data
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

    # Create full Pal entry
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

    # Update existing or add new
    if current_index is not None:
        data["pals"][current_index] = new_entry
    else:
        data["pals"].append(new_entry)
        current_index = len(data["pals"]) - 1

    save_json()
    refresh_list()


# ============================================================
# LIST REFRESH (update sidebar list)
# ============================================================

def refresh_list():
    """Reload Pal list in UI"""

    pal_listbox.delete(0, END)

    for pal in data["pals"]:
        pal_listbox.insert(END, f"#{pal['paldex_number']} - {pal['name']['display']}")


# ============================================================
# UI SETUP
# ============================================================

root = Tk()
root.state("zoomed")
root.minsize(800, 600)


# ============================================================
# MENU SCREEN
# ============================================================

menu_frame = Frame(root)

Button(menu_frame, text="Dex", command=lambda: show_frame(dex_frame)).pack()
Button(menu_frame, text="Editor", command=lambda: show_frame(editor_frame)).pack()


# ============================================================
# DEX SCREEN (view mode)
# ============================================================

dex_frame = Frame(root)

label_icon = Label(dex_frame)
label_icon.pack()

label_number = Label(dex_frame)
label_number.pack()

label_name = Label(dex_frame)
label_name.pack()

label_id = Label(dex_frame)
label_id.pack()

label_types = Label(dex_frame)
label_types.pack()

label_desc = Label(dex_frame, wraplength=400)
label_desc.pack()

Button(dex_frame, text="Prev", command=prev_pal).pack()
Button(dex_frame, text="Next", command=next_pal).pack()
Button(dex_frame, text="Back", command=lambda: show_frame(menu_frame)).pack()


# ============================================================
# EDITOR SCREEN (data editing UI)
# ============================================================

editor_frame = Frame(root)

# ----------------------------
# Pal list (left side)
# ----------------------------
pal_listbox = Listbox(editor_frame, width=30)
pal_listbox.grid(row=0, column=0, rowspan=50)
pal_listbox.bind("<<ListboxSelect>>", load_selected_pal)


# ----------------------------
# BASIC INFO FIELDS
# ----------------------------

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


# ============================================================
# WORK SUITABILITY SYSTEM (spinboxes)
# ============================================================

work_entries = {}
row = 6

# Auto-generate from JSON keys (future-proof)
work_keys = data["pals"][0]["work_suitability"].keys()

for key in work_keys:
    Label(editor_frame, text=key.replace("_", " ").title()).grid(row=row, column=1, sticky="w")

    e = Spinbox(editor_frame, from_=0, to=5, width=5)
    e.grid(row=row, column=2)

    work_entries[key] = e
    row += 1


# ============================================================
# ITEM DROPS SYSTEM
# ============================================================

entry_item_name = Entry(editor_frame)
entry_item_name.grid(row=row, column=1)

entry_item_chance = Entry(editor_frame)
entry_item_chance.grid(row=row+1, column=1)

entry_item_amount = Entry(editor_frame)
entry_item_amount.grid(row=row+2, column=1)

Button(editor_frame, text="Add Item", command=add_item).grid(row=row+3, column=1)

item_listbox = Listbox(editor_frame)
item_listbox.grid(row=row+4, column=1)


# ============================================================
# ACTION BUTTONS
# ============================================================

Button(editor_frame, text="New", command=new_pal).grid(row=row+5, column=1)
Button(editor_frame, text="Save", command=save_changes).grid(row=row+6, column=1)
Button(editor_frame, text="Back", command=lambda: show_frame(menu_frame)).grid(row=row+7, column=1)


# ============================================================
# START APP
# ============================================================

menu_frame.pack()
refresh_list()
root.mainloop()