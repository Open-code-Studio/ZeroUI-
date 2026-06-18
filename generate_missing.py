#!/usr/bin/env python3
"""Generate ALL 157 missing sprites: advancements, horse, toast, statistics, etc."""

from PIL import Image, ImageDraw
import os

BASE = os.path.join(os.path.dirname(__file__) or ".",
                     "assets", "minecraft", "textures", "gui", "sprites")
G = (74, 162, 111)
SC = (29, 27, 32, 255)
SCH = (33, 31, 38, 255)
OUT = (73, 69, 79, 255)

def save(path, img):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    img.save(full)

# ===== ADVANCEMENTS =====
def gen_advancements():
    # Boxes: 200x26
    for suffix, b in [("box_obtained", 180), ("box_unobtained", 80)]:
        img = Image.new("RGBA", (200, 26), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 200, 26), radius=6, fill=SC)
        d.rounded_rectangle((0, 0, 200, 26), radius=6, outline=OUT[:3] + (120,), width=1)
        save(f"advancements/{suffix}.png", img)

    # Title box: 200x26 L
    img = Image.new("L", (200, 26), 100)
    save("advancements/title_box.png", img)

    # Frames: 26x26
    for name, fill, mode in [
        ("challenge_frame_obtained", SC, "RGBA"),
        ("challenge_frame_unobtained", (100, 100, 100, 100), "LA"),
        ("goal_frame_obtained", (74, 162, 111, 80), "RGBA"),
        ("goal_frame_unobtained", (80, 80, 80, 80), "LA"),
        ("task_frame_obtained", SC, "RGBA"),
        ("task_frame_unobtained", (90, 90, 90, 90), "LA"),
    ]:
        if mode == "LA":
            img = Image.new("LA", (26, 26), (0, 0))
            if isinstance(fill, tuple):
                d = ImageDraw.Draw(img)
                d.rounded_rectangle((0, 0, 26, 26), radius=4, fill=(fill[0], fill[3]))
        else:
            img = Image.new("RGBA", (26, 26), (0,0,0,0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, 26, 26), radius=4, fill=fill)
        save(f"advancements/{name}.png", img)

    # Tabs: various sizes, LA mode
    tab_configs = [
        ("above_left", 28, 32), ("above_middle", 28, 32), ("above_right", 28, 32),
        ("below_left", 28, 32), ("below_middle", 28, 32), ("below_right", 28, 32),
        ("left_top", 32, 28), ("left_middle", 32, 28), ("left_bottom", 32, 28),
        ("right_top", 32, 28), ("right_middle", 32, 28), ("right_bottom", 32, 28),
    ]
    for name, w, h in tab_configs:
        for sel in [False, True]:
            b = 200 if sel else 100
            img = Image.new("LA", (w, h), (0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, w, h), radius=4, fill=(b, 255))
            s = "_selected" if sel else ""
            save(f"advancements/tab_{name}{s}.png", img)
    print("  Advancements: done")

# ===== HORSE / LLAMA =====
def gen_horse():
    for container in ["horse", "nautilus"]:
        # Slot backgrounds
        for name, size, mode in [
            ("armor_slot", (18, 18), "LA"),
            ("saddle_slot", (18, 18), "LA"),
        ]:
            img = Image.new("LA" if mode == "LA" else "RGBA", size, (0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, size[0], size[1]), radius=3, fill=(80, 200))
            save(f"container/{container}/{name}.png", img)

        # Nautilus armor slot for inventory
        if container == "nautilus":
            img = Image.new("LA", (18, 18), (0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, 18, 18), radius=3, fill=(80, 200))
            save("container/slot/nautilus_armor_inventory.png", img)
    print("  Horse/Llama/Nautilus: done")

# ===== BUNDLE =====
def gen_bundle():
    for name, size, fill in [
        ("bundle_progressbar_border", (12, 12), (150, 200)),
        ("bundle_progressbar_fill", (12, 12), (200, 255)),
        ("bundle_progressbar_full", (12, 12), (220, 255)),
        ("slot_background", (18, 18), (100, 200)),
        ("slot_highlight_back", (24, 24), (80, 200)),
        ("slot_highlight_front", (24, 24), (180, 200)),
    ]:
        img = Image.new("LA", size, (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, size[0], size[1]), radius=3, fill=fill)
        save(f"container/bundle/{name}.png", img)
    print("  Bundle: done")

# ===== SPECTATOR =====
def gen_spectator():
    for name, size in [
        ("scroll_left", (16, 16)), ("scroll_right", (16, 16)),
        ("teleport_to_player", (16, 16)), ("teleport_to_team", (16, 16)),
    ]:
        img = Image.new("LA", size, (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, size[0], size[1]), radius=4, fill=(150, 200))
        save(f"spectator/{name}.png", img)
    print("  Spectator: done")

# ===== STATISTICS =====
def gen_statistics():
    for name, size, mode in [
        ("block_mined", (18, 18), "RGBA"),
        ("item_broken", (18, 18), "RGBA"),
        ("item_crafted", (18, 18), "RGBA"),
        ("item_dropped", (18, 18), "RGBA"),
        ("item_picked_up", (18, 18), "RGBA"),
        ("item_used", (18, 18), "RGBA"),
    ]:
        img = Image.new(mode, size, (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, size[0], size[1]), radius=3, fill=SC)
        save(f"statistics/{name}.png", img)

    for name, size in [("header", (18, 18)), ("sort_down", (18, 18)), ("sort_up", (18, 18))]:
        img = Image.new("LA", size, (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, size[0], size[1]), radius=3, fill=(120, 200))
        save(f"statistics/{name}.png", img)
    print("  Statistics: done")

# ===== TOAST NOTIFICATIONS =====
def gen_toast():
    # Advancement toast: 160x32
    for name, size in [
        ("advancement", (160, 32)), ("now_playing", (160, 32)),
        ("recipe", (160, 32)), ("tutorial", (160, 32)),
    ]:
        img = Image.new("RGBA", size, (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, size[0], size[1]), radius=8, fill=SC)
        d.rounded_rectangle((0, 0, size[0], size[1]), radius=8, outline=OUT[:3] + (120,), width=1)
        save(f"toast/{name}.png", img)

    # System toast: 160x64
    img = Image.new("RGBA", (160, 64), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, 160, 64), radius=8, fill=SC)
    d.rounded_rectangle((0, 0, 160, 64), radius=8, outline=OUT[:3] + (120,), width=1)
    save("toast/system.png", img)

    # Small icon toasts: 20x20
    for name, mode, b in [
        ("mouse", "LA", 150), ("movement_keys", "L", 150),
        ("recipe_book", "L", 150), ("right_click", "RGBA", None),
        ("social_interactions", "L", 150), ("tree", "L", 150),
        ("wooden_planks", "L", 150),
    ]:
        if mode == "RGBA":
            img = Image.new("RGBA", (20, 20), (0,0,0,0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, 20, 20), radius=4, fill=SC)
        elif mode == "LA":
            img = Image.new("LA", (20, 20), (0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, 20, 20), radius=4, fill=(b, 200))
        else:
            img = Image.new("L", (20, 20), b)
        save(f"toast/{name}.png", img)
    print("  Toast: done")

# ===== TRANSFERABLE LIST =====
def gen_transferable():
    for name, mode, b in [
        ("move_down", "RGBA", None), ("move_up", "RGBA", None),
        ("select", "RGBA", None), ("unselect", "LA", 150),
    ]:
        for hl in [False, True]:
            sfx = "_highlighted" if hl else ""
            if mode == "RGBA":
                img = Image.new("RGBA", (32, 32), (0,0,0,0))
                d = ImageDraw.Draw(img)
                fill = SCH if hl else SC
                d.rounded_rectangle((2, 2, 30, 30), radius=6, fill=fill)
            else:
                val = 200 if hl else b
                img = Image.new("LA", (32, 32), (0, 0))
                d = ImageDraw.Draw(img)
                d.rounded_rectangle((2, 2, 30, 30), radius=6, fill=(val, 255))
            save(f"transferable_list/{name}{sfx}.png", img)
    print("  Transferable list: done")

# ===== DISABLED LOCK BUTTONS =====
def gen_disabled_locks():
    for prefix in ["locked", "unlocked"]:
        img = Image.new("L", (20, 20), 0)
        d = ImageDraw.Draw(img)
        b = 60
        d.rectangle((4, 8, 16, 18), fill=b if "locked" in prefix else 0, outline=b, width=2)
        d.arc((6, 2, 14, 10), 180, 0, fill=b, width=2)
        save(f"widget/{prefix}_button_disabled.png", img)
    print("  Disabled lock buttons: done")

# ===== REMAINING SLOT ICONS =====
def gen_slot_icons():
    slot_icons = [
        "chestplate", "leggings", "boots", "helmet",
        "pickaxe", "shovel", "sword", "spear",
        "potion", "quartz", "redstone_dust", "saddle",
        "shield", "smithing_template_armor_trim", "smithing_template_netherite_upgrade",
    ]
    for name in slot_icons:
        img = Image.new("LA", (18, 18), (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 18, 18), radius=3, fill=(80, 200))
        save(f"container/slot/{name}.png", img)
    print("  Slot icons: done")

# ===== MAIN =====
def main():
    print("Generating 157 missing sprites...")
    gen_advancements()
    gen_horse()
    gen_bundle()
    gen_spectator()
    gen_statistics()
    gen_toast()
    gen_transferable()
    gen_disabled_locks()
    gen_slot_icons()
    print("All missing sprites generated!")

if __name__ == "__main__":
    main()
