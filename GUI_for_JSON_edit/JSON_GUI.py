from tkinter import *
from tkinter import filedialog
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
ICON_DIR = os.path.join(BASE_DIR, "..", "assets", "Pal_Icons")

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
editor_item_drops = []
selected_editor_item = None


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

    work_lines = [
        f"{'Task':<30}Value",
        f"{'-' * 30} {'-' * 5}"
    ]
    work_lines.extend(
        f"{key.replace('_', ' ').title():<30}{value}"
        for key, value in pal["work_suitability"].items()
    )
    label_work_suitability.config(text="\n".join(work_lines))

    item_drops_listbox.delete(0, END)
    item_drops_listbox.insert(END, f"{'Name':<24}{'Dropchance':<12}{'Amount':<8}")
    item_drops_listbox.insert(END, "".ljust(46, "-"))
    if pal.get("item_drops"):
        for item in pal["item_drops"]:
            item_drops_listbox.insert(
                END,
                f"{item['item_name'][:22]:<24}{item['drop_chance']:<12}{item['amount']:<8}"
            )
    else:
        item_drops_listbox.insert(END, "No item drops")

    try:
        icon_name = os.path.basename(pal["icon_path"])
        icon_path = os.path.join(ICON_DIR, icon_name)

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

    icon_name = os.path.basename(icon_name)
    icon_path = os.path.join(ICON_DIR, icon_name)

    try:
        img = Image.open(icon_path)
        img = img.resize((80, 80))

        current_image = ImageTk.PhotoImage(img)
        label_icon_preview.config(image=current_image, text="")

    except:
        label_icon_preview.config(text="Icon not found", image="")


def browse_icon():
    file_path = filedialog.askopenfilename(
        initialdir=ICON_DIR,
        title="Select Pal icon",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*")]
    )
    if not file_path:
        return

    entry_icon.delete(0, END)
    entry_icon.insert(0, os.path.basename(file_path))
    preview_icon()


def refresh_editor_item_list():
    item_listbox.delete(0, END)
    item_listbox.insert(END, f"{'Name':<24}{'Dropchance':<12}{'Amount':<8}")
    item_listbox.insert(END, "".ljust(46, "-"))

    if editor_item_drops:
        for item in editor_item_drops:
            item_listbox.insert(
                END,
                f"{item['item_name'][:22]:<24}{item['drop_chance']:<12}{item['amount']:<8}"
            )
    else:
        item_listbox.insert(END, "No item drops")

    if selected_editor_item is not None and 0 <= selected_editor_item < len(editor_item_drops):
        item_listbox.selection_clear(0, END)
        item_listbox.selection_set(selected_editor_item + 2)


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
    entry_icon.insert(0, os.path.basename(pal["icon_path"]))
    preview_icon()

    text_desc.delete("1.0", END)
    text_desc.insert("1.0", pal["description"])

    for key in work_entries:
        work_entries[key].delete(0, END)
        work_entries[key].insert(0, pal["work_suitability"].get(key, 0))

    editor_item_drops.clear()
    editor_item_drops.extend(pal["item_drops"])
    clear_selected_editor_item()
    refresh_editor_item_list()


# ============================================================
# EDITOR ITEM SELECTION

def clear_selected_editor_item():
    global selected_editor_item
    selected_editor_item = None


def load_selected_editor_item(event):
    global selected_editor_item

    selection = item_listbox.curselection()
    if not selection:
        return

    item_index = selection[0] - 2
    if item_index < 0 or item_index >= len(editor_item_drops):
        clear_selected_editor_item()
        return

    selected_editor_item = item_index
    item = editor_item_drops[item_index]

    entry_item_name.delete(0, END)
    entry_item_name.insert(0, item["item_name"])

    entry_item_chance.delete(0, END)
    entry_item_chance.insert(0, item["drop_chance"])

    entry_item_amount.delete(0, END)
    entry_item_amount.insert(0, item["amount"])


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

    editor_item_drops.clear()
    refresh_editor_item_list()


# ============================================================
# ADD ITEM
# ============================================================

def add_item():
    global selected_editor_item

    name = entry_item_name.get().strip()
    chance = entry_item_chance.get().strip()
    amount = entry_item_amount.get().strip()

    if name:
        editor_item_drops.append({
            "item_name": name,
            "drop_chance": chance,
            "amount": amount
        })
        selected_editor_item = len(editor_item_drops) - 1
        refresh_editor_item_list()


def update_item():
    global selected_editor_item

    if selected_editor_item is None:
        return

    name = entry_item_name.get().strip()
    chance = entry_item_chance.get().strip()
    amount = entry_item_amount.get().strip()

    if not name:
        return

    editor_item_drops[selected_editor_item] = {
        "item_name": name,
        "drop_chance": chance,
        "amount": amount
    }
    refresh_editor_item_list()


def remove_item():
    global selected_editor_item

    if selected_editor_item is None:
        return

    del editor_item_drops[selected_editor_item]
    clear_selected_editor_item()
    refresh_editor_item_list()


# ============================================================
# SAVE
# ============================================================

def save_changes():
    global current_index

    work_data = {k: int(work_entries[k].get()) for k in work_entries}
    item_drops = list(editor_item_drops)

    new_entry = {
        "paldex_number": entry_number.get(),
        "name": {
            "display": entry_name.get(),
            "internal_id": entry_id.get()
        },
        "icon_path": f"../assets/Pal_Icons/{os.path.basename(entry_icon.get().strip())}",
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

    editor_item_drops.clear()
    editor_item_drops.extend(new_entry["item_drops"])

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

Button(menu_buttons_frame, text="Dex", command=lambda: show_frame(dex_frame), font=("Arial", 18)).pack()
Button(menu_buttons_frame, text="Editor", command=lambda: show_frame(editor_frame), font=("Arial", 18)).pack()


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

label_work_suitability = Label(dex_right, wraplength=400, justify=LEFT, font=("Courier New", 10))
label_work_suitability.pack()

Label(dex_right, text="Item Drops:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 0))
item_drops_listbox = Listbox(dex_right, width=50, height=6, font=("Courier New", 10))
item_drops_listbox.pack(fill="x")

Button(dex_right, text="Prev", command=prev_pal, font=("Arial", 18)).pack()
Button(dex_right, text="Next", command=next_pal, font=("Arial", 18)).pack()
Button(dex_right, text="Back", command=lambda: show_frame(menu_frame), font=("Arial", 18)).pack()

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

Label(editor_frame, text="Icon filename").grid(row=5, column=1, sticky="w")
entry_icon = Entry(editor_frame)
entry_icon.grid(row=5, column=2)
Button(editor_frame, text="Browse", command=lambda: browse_icon(), font=("Arial", 12)).grid(row=5, column=3, padx=5)

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

Button(editor_frame, text="➕ Add Item", command=add_item, font=("Arial", 18)).grid(row=row, column=1)
Button(editor_frame, text="✏️ Edit Item", command=update_item, font=("Arial", 18)).grid(row=row, column=2)
Button(editor_frame, text="🗑️ Delete Item", command=remove_item, font=("Arial", 18)).grid(row=row, column=3)
row += 1

item_listbox = Listbox(editor_frame, width=50, height=8, font=("Courier New", 10))
item_listbox.grid(row=row, column=1, columnspan=3)
item_listbox.bind("<<ListboxSelect>>", load_selected_editor_item)
row += 1

Button(editor_frame, text="New Pal", command=new_pal, font=("Arial", 18)).grid(row=row, column=1)
Button(editor_frame, text="Save Pal", command=save_changes, font=("Arial", 18)).grid(row=row, column=2)
Button(editor_frame, text="Back", command=lambda: show_frame(menu_frame), font=("Arial", 18)).grid(row=row, column=3)


# ============================================================
# START
# ============================================================

menu_frame.pack(side=TOP, fill="x", pady=10)
refresh_all_listboxes()
root.mainloop()