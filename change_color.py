#!/usr/bin/env python3
"""
ZeroUI - Color Changer
Change the primary color of entire ZeroUI resource pack.
Edit color.conf then run: python3 change_color.py
"""

import os, sys, json
from PIL import Image, ImageDraw

def hex_to_rgba(hex_str):
    """Convert RRGGBB hex to RGBA tuple."""
    h = hex_str.strip().lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)

def read_config():
    """Read color.conf, return primary RGBA tuple."""
    conf_path = os.path.join(os.path.dirname(__file__) or ".", "color.conf")
    color = "4AA26F"  # default
    try:
        with open(conf_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("PRIMARY=") and not line.startswith("#"):
                    color = line.split("=")[1].strip()
                    break
    except FileNotFoundError:
        pass
    return hex_to_rgba(color)

def regenerate_all(primary):
    """Regenerate all sprites with the given primary color."""
    G = primary
    GD = tuple(max(0, c // 3) for c in G[:3]) + (255,)  # dark variant
    GL = tuple(min(255, c + 80) for c in G[:3]) + (255,)  # light variant

    S = (20, 18, 24, 255)
    SC = (29, 27, 32, 255)
    SCH = (33, 31, 38, 255)
    OS = (230, 224, 233, 255)
    OUT = (73, 69, 79, 255)

    BASE = os.path.join(os.path.dirname(__file__) or ".",
                         "assets", "minecraft", "textures", "gui", "sprites")

    def save(path, img):
        full = os.path.join(BASE, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        img.save(full)

    print(f"Regenerating with PRIMARY={G}")

    # ---- BUTTONS ----
    for name, h, b in [("button.png", 20, 140), ("button_disabled.png", 20, 50)]:
        img = Image.new("L", (200, h), 0)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 200, h), fill=b)
        save(f"widget/{name}", img)

    # Highlighted button with green border
    img = Image.new("RGBA", (200, 20), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 200, 20), fill=G[:3] + (200,))
    b2 = tuple(min(255, c + 30) for c in G[:3]) + (255,)
    d.rectangle((0, 0, 200, 20), outline=b2, width=2)
    save("widget/button_highlighted.png", img)

    # ---- TEXT FIELDS ----
    for hl in [False, True]:
        img = Image.new("RGBA", (200, 20), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 200, 20), fill=SC)
        outline_c = G[:3] + (200,) if hl else OUT[:3] + (80,)
        d.rectangle((0, 0, 200, 20), outline=outline_c, width=2 if hl else 1)
        save(f"widget/text_field{'_highlighted' if hl else ''}.png", img)

    # ---- SLIDERS ----
    for name, w, h, b in [("slider", 200, 20, 100), ("slider_handle", 8, 20, 170)]:
        img = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, w, h), fill=b)
        save(f"widget/{name}.png", img)

    img = Image.new("RGBA", (200, 20), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 200, 20), fill=G[:3] + (200,))
    save("widget/slider_highlighted.png", img)

    img = Image.new("RGBA", (8, 20), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 8, 20), fill=G[:3] + (200,))
    save("widget/slider_handle_highlighted.png", img)

    # ---- CHECKBOXES ----
    for sel in [False, True]:
        for hl in [False, True]:
            img = Image.new("L", (20, 20), 0)
            d = ImageDraw.Draw(img)
            b = 220 if hl else 150
            d.rectangle((1, 1, 19, 19), outline=b, width=2)
            if sel:
                d.rectangle((3, 3, 17, 17), fill=b)
            name = f"checkbox{'_selected' if sel else ''}{'_highlighted' if hl else ''}"
            save(f"widget/{name}.png", img)

    # ---- LOCK BUTTONS ----
    for locked in [True, False]:
        for hl in [False, True]:
            img = Image.new("L", (20, 20), 0)
            d = ImageDraw.Draw(img)
            b = 230 if hl else 150
            d.rectangle((4, 8, 16, 18), fill=b if locked else 0, outline=b, width=2)
            d.arc((6, 2, 14, 10), 180, 0, fill=b, width=2)
            pfx = "locked" if locked else "unlocked"
            sfx = "_highlighted" if hl else ""
            save(f"widget/{pfx}_button{sfx}.png", img)

    # ---- CROSS BUTTON ----
    for sfx, b in [("", 150), ("_highlighted", 220)]:
        img = Image.new("L", (14, 14), 0)
        d = ImageDraw.Draw(img)
        d.line((2, 2, 12, 12), fill=b, width=2)
        d.line((12, 2, 2, 12), fill=b, width=2)
        save(f"widget/cross_button{sfx}.png", img)

    # ---- PAGE NAV ----
    for dir_ in ["forward", "backward"]:
        for sfx, b in [("", 140), ("_highlighted", 220)]:
            img = Image.new("L", (23, 13), 0)
            d = ImageDraw.Draw(img)
            d.rectangle((0, 0, 23, 13), fill=b)
            pts = [(10, 3), (18, 6), (10, 9)] if dir_ == "forward" else [(13, 3), (5, 6), (13, 9)]
            d.polygon(pts, fill=0)
            save(f"widget/page_{dir_}{sfx}.png", img)

    # ---- SCROLLERS ----
    for w, h, paths in [
        (6, 32, ["widget/scroller"]),
        (12, 15, [f"container/{c}/scroller" for c in ["creative_inventory", "loom", "stonecutter"]]),
        (6, 27, ["container/villager/scroller"]),
    ]:
        for p in paths:
            for sfx, b in [("", 180), ("_disabled", 80)]:
                img = Image.new("L", (w, h), 0)
                d = ImageDraw.Draw(img)
                d.rectangle((0, 0, w, h), fill=b)
                save(f"{p}{sfx}.png", img)

    # ---- WIDGET TABS ----
    for name in ["tab", "tab_highlighted", "tab_selected", "tab_selected_highlighted"]:
        sel = "selected" in name
        hl_ = "highlighted" in name
        b = 220 if sel else 120
        if hl_: b = min(255, b + 40)
        img = Image.new("LA", (130, 24), (0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 130, 24), fill=(b, 255))
        save(f"widget/{name}.png", img)

    # ---- SLOT HIGHLIGHTS ----
    for name in ["slot_highlight_back", "slot_highlight_front"]:
        img = Image.new("LA", (24, 24), (0, 0))
        d = ImageDraw.Draw(img)
        if "back" in name:
            d.rectangle((0, 0, 24, 24), fill=(40, 200))
        else:
            d.rectangle((1, 1, 23, 23), outline=(200, 200), width=2)
        save(f"container/{name}.png", img)

    # ---- CREATIVE TABS ----
    for i in range(1, 8):
        for top in [True, False]:
            for sel in [True, False]:
                b = 200 if sel else 100
                img = Image.new("LA", (26, 32), (0, 0))
                d = ImageDraw.Draw(img)
                if top:
                    d.rectangle((0, 0, 26, 32), fill=(b, 255))
                    d.rectangle((0, 26, 26, 32), fill=(b, 255))
                else:
                    d.rectangle((0, 4, 26, 32), fill=(b, 255))
                    d.rectangle((0, 4, 26, 10), fill=(b, 255))
                v = "top" if top else "bottom"
                s = "selected" if sel else "unselected"
                save(f"container/creative_inventory/tab_{v}_{s}_{i}.png", img)

    # ---- BOSS BARS ----
    colors = {
        "pink": (255,100,180), "blue": (100,150,255), "red": (255,80,80),
        "green": (80,200,120), "yellow": (255,220,60), "purple": (180,120,255),
    }
    for name, (r,g,b) in colors.items():
        for suffix, fill in [("background", (29,27,32,255)), ("progress", (r,g,b,255))]:
            img = Image.new("RGBA", (182, 5), (0,0,0,0))
            d = ImageDraw.Draw(img)
            d.rectangle((0, 0, 182, 5), fill=fill)
            save(f"boss_bar/{name}_{suffix}.png", img)
    # White
    for suffix, b in [("background", 80), ("progress", 200)]:
        img = Image.new("L", (182, 5), b)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 182, 5), fill=b)
        save(f"boss_bar/white_{suffix}.png", img)
    # Notched
    for n in [6, 10, 12, 20]:
        seg = 182 // n
        for suffix, b in [("background", 80), ("progress", 200)]:
            img = Image.new("LA", (182, 5), (b, 255))
            d = ImageDraw.Draw(img)
            for i in range(n):
                if i % 2 == 1:
                    d.rectangle((i*seg, 0, (i+1)*seg, 5), fill=(30, 255))
            save(f"boss_bar/notched_{n}_{suffix}.png", img)

    # ---- HUD SPRITES (hearts, hotbar, etc.) ----
    # These use hardcoded colors (red for hearts, orange for food, etc.) not primary color
    # So they don't need re-generation

    # ---- SCREEN BACKGROUNDS ----
    for size, path in [(236, "social_interactions"), (236, "popup")]:
        img = Image.new("L", (size, 34), 40)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, size, 34), fill=60)
        save(f"{path}/background.png", img)

    # Tooltip with green border
    img = Image.new("RGBA", (100, 100), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 100, 100), fill=(33, 31, 38, 240))
    d.rectangle((0, 0, 100, 100), outline=OUT[:3] + (150,), width=1)
    save("tooltip/background.png", img)

    img = Image.new("RGBA", (100, 100), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 100, 100), outline=G[:3] + (180,), width=2)
    save("tooltip/frame.png", img)

    # ---- RECIPE BOOK ----
    for sfx, b in [("", 120), ("_highlighted", 200)]:
        img = Image.new("RGBA", (20, 18), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 20, 18), fill=SC)
        save(f"recipe_book/button{sfx}.png", img)

    for d_ in ["forward", "backward"]:
        for sfx, b in [("", 120), ("_highlighted", 200)]:
            img = Image.new("LA", (12, 17), (0, 0))
            d = ImageDraw.Draw(img)
            d.rectangle((0, 0, 12, 17), fill=(b, 255))
            save(f"recipe_book/page_{d_}{sfx}.png", img)

    # ---- SERVER/WORLD ICONS ----
    for pfx in ["server_list", "world_list"]:
        for name, mode in [("join", "LA"), ("move_up", "L"), ("move_down", "L")]:
            if pfx == "world_list" and "move" in name: continue
            for sfx, b in [("", 160), ("_highlighted", 220)]:
                img = Image.new(mode, (32, 32), 0)
                d = ImageDraw.Draw(img)
                fill_val = (b, 255) if mode == "LA" else b
                d.rectangle((2, 2, 30, 30), fill=fill_val)
                save(f"{pfx}/{name}{sfx}.png", img)

    print(f"\nDone! All sprites regenerated with PRIMARY = {G}")
    print(f"Color: #{G[0]:02X}{G[1]:02X}{G[2]:02X}")


if __name__ == "__main__":
    primary = read_config()
    regenerate_all(primary)

    # Sync to resourcepacks
    import subprocess
    src = os.path.join(os.path.dirname(__file__) or ".", "assets")
    dst = os.path.expanduser("~/Library/Application Support/minecraft/versions/1.21.11/resourcepacks/ZeroUI-/assets")
    subprocess.run(["rm", "-rf", dst])
    subprocess.run(["cp", "-r", src, dst])
    print(f"Synced to resourcepacks!")
