from tkinter import *
import os
import json
from PIL import Image, ImageTk

# ============================================================
# NOTE
# AI-generated editor tool for managing Pal JSON data.
# ============================================================

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "..", "JSON's", "Pals.json")
ICON_DIR = os.path.join(BASE_DIR, "..", "Icons")

# ============================================================
# JSON HANDLING
# ============================================================

def load_json():
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_json():
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

data = load_json()
current_index = 0
current_image = None


# ============================================================
# FRAME SWITCHING
# ============================================================

def show_frame(frame):
    menu_frame.pack_forget()
    dex_frame.pack_forget()
    editor_frame.pack_forget()
    frame.pack(fill="both", expand=True)

    # Auto-select first Pal when opening Dex
    if frame == dex_frame and data["pals"]:
        display_pal(current_index)
        select_dex_item()


# ============================================================
# DEX VIEW (DISPLAY)
# ============================================================

def display_pal(index):
    global current_image

    pal = data["pals"][index]

    label_number.config(text=f"#{pal['paldex_number']}")
    label_name.config(text=pal["name"]["display"])
    label_id.config(text=f"ID: {pal['name']['internal_id']}")
    label_types.config(text=" / ".join(pal["types"]))
    label_desc.config(text=pal["description"])

    work_text = "\n".join(
        f"{key}: {value}" for key, value in pal["work_suitability"].items()
    )
    label_work_suitability.config(text=work_text)

    if pal.get("item_drops"):
        item_lines = []
        for item in pal["item_drops"]:
            item_lines.append(
                f"Name: {item['item_name']}\nDropchance: {item['drop_chance']}\nAmount: {item['amount']}"
            )
        item_text = "\n\n".join(item_lines)
    else:
        item_text = "No item drops"
    label_item_drops.config(text=item_text)

    try:
        icon_path = os.path.join(ICON_DIR, pal["icon_path"])

        img = Image.open(icon_path)
        img = img.resize((80, 80))

        current_image = ImageTk.PhotoImage(img)
        label_icon.config(image=current_image, text="")

    except:
        label_icon.config(text="No Image", image="")


# ============================================================
# DEX NAVIGATION
# ============================================================

def next_pal():
    global current_index
    if current_index < len(data["pals"]) - 1:
        current_index += 1
        display_pal(current_index)
        select_dex_item()


def prev_pal():
    global current_index
    if current_index > 0:
        current_index -= 1
        display_pal(current_index)
        select_dex_item()


# ============================================================
# DEX LIST CONTROL (NEW)
# ============================================================

def load_dex_selection(event):
    global current_index

    selection = dex_listbox.curselection()
    if not selection:
        return

    current_index = selection[0]
    display_pal(current_index)


def select_dex_item():
    dex_listbox.selection_clear(0, END)
    dex_listbox.selection_set(current_index)
    dex_listbox.see(current_index)


def refresh_dex():
    dex_listbox.delete(0, END)

    for pal in data["pals"]:
        dex_listbox.insert(
            END,
            f"#{pal['paldex_number']} - {pal['name']['display']}"
        )


# ============================================================
# ICON PREVIEW
# ============================================================

def preview_icon():
    global current_image

    icon_name = entry_icon.get().strip()
    if not icon_name:
        label_icon_preview.config(text="No Preview", image="")
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
# LOAD SELECTED PAL INTO EDITOR
# ============================================================

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
    preview_icon()

    text_desc.delete("1.0", END)
    text_desc.insert("1.0", pal["description"])

    for key in work_entries:
        work_entries[key].delete(0, END)
        work_entries[key].insert(0, pal["work_suitability"].get(key, 0))

    item_listbox.delete(0, END)
    for item in pal["item_drops"]:
        item_listbox.insert(END, f"{item['item_name']}|{item['drop_chance']}|{item['amount']}")


# ============================================================
# NEW PAL
# ============================================================

def new_pal():
    global current_index
    current_index = None

    entry_number.delete(0, END)
    entry_name.delete(0, END)
    entry_id.delete(0, END)
    entry_types.delete(0, END)
    entry_icon.delete(0, END)
    text_desc.delete("1.0", END)
    label_icon_preview.config(text="No Preview", image="")

    for key in work_entries:
        work_entries[key].delete(0, END)
        work_entries[key].insert(0, "0")

    item_listbox.delete(0, END)


# ============================================================
# ADD ITEM
# ============================================================

def add_item():
    name = entry_item_name.get()
    chance = entry_item_chance.get()
    amount = entry_item_amount.get()

    if name:
        item_listbox.insert(END, f"{name}|{chance}|{amount}")


# ============================================================
# SAVE
# ============================================================

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
    refresh_all_listboxes()


# ============================================================
# UI ROOT
# ============================================================

root = Tk()
root.state("zoomed")
root.minsize(800, 600)


# ============================================================
# MENU (UNCHANGED)
# ============================================================

menu_frame = Frame(root)

Label(menu_frame, text="Palworld JSON Editor", font=("Arial", 24)).pack(side=TOP, pady=20)

menu_buttons_frame = Frame(menu_frame)
menu_buttons_frame.pack(side=LEFT, pady=30)

Button(menu_buttons_frame, text="Dex", command=lambda: show_frame(dex_frame)).pack()
Button(menu_buttons_frame, text="Editor", command=lambda: show_frame(editor_frame)).pack()


# ============================================================
# DEX VIEW (NOW FULL POKEDEX STYLE)
# ============================================================

dex_frame = Frame(root)

# LEFT LIST
dex_left = Frame(dex_frame)
dex_left.pack(side=LEFT, fill=Y)

dex_listbox = Listbox(dex_left, width=35)
dex_listbox.pack(side=LEFT, fill=Y)

dex_scroll = Scrollbar(dex_left)
dex_scroll.pack(side=RIGHT, fill=Y)

dex_listbox.config(yscrollcommand=dex_scroll.set)
dex_scroll.config(command=dex_listbox.yview)

dex_listbox.bind("<<ListboxSelect>>", load_dex_selection)


# RIGHT DETAILS
dex_right = Frame(dex_frame)
dex_right.pack(side=LEFT, fill=BOTH, expand=True)

label_icon = Label(dex_right)
label_icon.pack()

label_number = Label(dex_right)
label_number.pack()

label_name = Label(dex_right)
label_name.pack()

label_id = Label(dex_right)
label_id.pack()

label_types = Label(dex_right)
label_types.pack()

label_desc = Label(dex_right, wraplength=400)
label_desc.pack()

label_work_suitability = Label(dex_right, wraplength=400, justify=LEFT)
label_work_suitability.pack()

label_item_drops = Label(dex_right, wraplength=400, justify=LEFT)
label_item_drops.pack()

Button(dex_right, text="Prev", command=prev_pal).pack()
Button(dex_right, text="Next", command=next_pal).pack()
Button(dex_right, text="Back", command=lambda: show_frame(menu_frame)).pack()

# ============================================================
# refresh_all_listboxes() - NEW FUNCTION TO REFRESH BOTH LISTBOXES
# ============================================================

def refresh_all_listboxes():
    # Refresh dex listbox
    dex_listbox.delete(0, END)
    # Refresh pal listbox
    pal_listbox.delete(0, END)
    
    for pal in data["pals"]:
        display_text = f"#{pal['paldex_number']} - {pal['name']['display']}"
        dex_listbox.insert(END, display_text)
        pal_listbox.insert(END, display_text)

# ============================================================
# EDITOR (UNCHANGED)
# ============================================================

editor_frame = Frame(root)
pal_listbox = Listbox(editor_frame, width=30)
pal_listbox.grid(row=0, column=0, rowspan=100, sticky="ns")
pal_listbox.bind("<<ListboxSelect>>", load_selected_pal)


# BASIC INFO
Label(editor_frame, text="=== BASIC INFO ===").grid(row=0, column=1, sticky="w")

Label(editor_frame, text="Number").grid(row=1, column=1, sticky="w")
entry_number = Entry(editor_frame)
entry_number.grid(row=1, column=2)

Label(editor_frame, text="Name").grid(row=2, column=1, sticky="w")
entry_name = Entry(editor_frame)
entry_name.grid(row=2, column=2)

Label(editor_frame, text="Internal ID").grid(row=3, column=1, sticky="w")
entry_id = Entry(editor_frame)
entry_id.grid(row=3, column=2)

Label(editor_frame, text="Types").grid(row=4, column=1, sticky="w")
entry_types = Entry(editor_frame)
entry_types.grid(row=4, column=2)

Label(editor_frame, text="Icon").grid(row=5, column=1, sticky="w")
entry_icon = Entry(editor_frame)
entry_icon.grid(row=5, column=2)

label_icon_preview = Label(editor_frame, text="No Preview")
label_icon_preview.grid(row=6, column=3)

Label(editor_frame, text="Description").grid(row=6, column=1, sticky="nw")
text_desc = Text(editor_frame, height=5, width=30)
text_desc.grid(row=6, column=2)


# WORK + ITEMS + BUTTONS (UNCHANGED)
row = 7

Label(editor_frame, text="=== WORK SUITABILITY ===").grid(row=row, column=1, sticky="w")
row += 1

work_entries = {}
work_keys = data["pals"][0]["work_suitability"].keys()

for key in work_keys:
    Label(editor_frame, text=key.replace("_", " ").title()).grid(row=row, column=1, sticky="w")
    e = Spinbox(editor_frame, from_=0, to=5, width=5)
    e.grid(row=row, column=2)
    work_entries[key] = e
    row += 1

Label(editor_frame, text="=== ITEM DROPS ===").grid(row=row, column=1, sticky="w")
row += 1

Label(editor_frame, text="Item Name").grid(row=row, column=1, sticky="w")
entry_item_name = Entry(editor_frame)
entry_item_name.grid(row=row, column=2)
row += 1

Label(editor_frame, text="Drop Chance").grid(row=row, column=1, sticky="w")
entry_item_chance = Entry(editor_frame)
entry_item_chance.grid(row=row, column=2)
row += 1

Label(editor_frame, text="Amount").grid(row=row, column=1, sticky="w")
entry_item_amount = Entry(editor_frame)
entry_item_amount.grid(row=row, column=2)
row += 1

Button(editor_frame, text="➕ Add Item", command=add_item).grid(row=row, column=2)
row += 1

item_listbox = Listbox(editor_frame, width=40)
item_listbox.grid(row=row, column=1, columnspan=2)
row += 1

Button(editor_frame, text="New Pal", command=new_pal).grid(row=row, column=1)
Button(editor_frame, text="Save Pal", command=save_changes).grid(row=row, column=2)
Button(editor_frame, text="Back", command=lambda: show_frame(menu_frame)).grid(row=row, column=3)


# ============================================================
# START
# ============================================================

menu_frame.pack(side=TOP, fill="x", pady=10)
refresh_all_listboxes()
root.mainloop()