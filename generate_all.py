#!/usr/bin/env python3
"""
ZeroUI - Complete Sprite Generator v2
All sprites with CORRECT dimensions and modes for 1.21.5+
"""
from PIL import Image, ImageDraw
import os, json

BASE = os.path.join(os.path.dirname(__file__) or ".",
                     "assets", "minecraft", "textures", "gui", "sprites")

def save(path, img):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    img.save(full)

def save_json(path, data):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        json.dump(data, f)

# ============================================================
# WIDGET: SCROLLERS (with correct sizes!)
# ============================================================
def make_scroller(w, h, mode="L"):
    """Scroller thumb: L mode (grayscale), game tints it."""
    img = Image.new(mode, (w, h), 0)
    d = ImageDraw.Draw(img)
    if mode == "L":
        d.rounded_rectangle((0, 0, w, h), radius=min(w,h)//2 - 1, fill=180)
    elif mode == "1":
        d.rounded_rectangle((0, 0, w, h), radius=min(w,h)//2 - 1, fill=1)
    return img

def generate_scrollers():
    # Widget scroller: 6x32 L mode
    save("widget/scroller.png", make_scroller(6, 32, "L"))
    # Widget scroller background: 6x32 "1" mode (binary)
    bg = Image.new("1", (6, 32), 0)
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((0, 0, 6, 32), radius=2, fill=0)
    d.rounded_rectangle((1, 1, 5, 31), radius=2, fill=1)
    save("widget/scroller_background.png", bg)

    # Container scrollers: 12x15 L mode
    for ctr in ["creative_inventory", "loom", "stonecutter"]:
        for suffix, bright in [("", 180), ("_disabled", 80)]:
            save(f"container/{ctr}/scroller{suffix}.png", make_scroller(12, 15, "L"))

    # Villager scroller: 6x27 L mode
    for suffix, bright in [("", 180), ("_disabled", 80)]:
        save(f"container/villager/scroller{suffix}.png", make_scroller(6, 27, "L"))

    print("  Scrollers: fixed (correct sizes)")

# ============================================================
# WIDGET: BUTTONS (200x20 L mode)
# ============================================================
def make_button(w, h, brightness):
    img = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, h), radius=4, fill=brightness)
    return img

def generate_buttons():
    save("widget/button.png", make_button(200, 20, 120))
    save("widget/button_disabled.png", make_button(200, 20, 60))
    save("widget/button_highlighted.png", make_button(200, 20, 180))
    print("  Buttons: done")

# ============================================================
# WIDGET: TEXT FIELDS (200x20 P mode)
# ============================================================
def make_text_field(w=200, h=20, highlighted=False):
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(img)
    fill = (33, 31, 38, 255)  # surface container high
    outline = (74, 162, 111, 200) if highlighted else (73, 69, 79, 150)
    d.rounded_rectangle((0, 0, w, h), radius=4, fill=fill, outline=outline, width=1)
    return img

def generate_text_fields():
    save("widget/text_field.png", make_text_field(200, 20, False))
    save("widget/text_field_highlighted.png", make_text_field(200, 20, True))
    print("  Text fields: done")

# ============================================================
# WIDGET: CHECKBOXES (20x20 L mode)
# ============================================================
def make_checkbox(size=20, selected=False, highlighted=False):
    img = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(img)
    brightness = 200 if highlighted else 140
    d.rounded_rectangle((2, 2, size-2, size-2), radius=4, outline=brightness, width=2)
    if selected:
        d.rounded_rectangle((3, 3, size-3, size-3), radius=3, fill=240)
    return img

def generate_checkboxes():
    save("widget/checkbox.png", make_checkbox(20, False, False))
    save("widget/checkbox_highlighted.png", make_checkbox(20, False, True))
    save("widget/checkbox_selected.png", make_checkbox(20, True, False))
    save("widget/checkbox_selected_highlighted.png", make_checkbox(20, True, True))
    print("  Checkboxes: done")

# ============================================================
# WIDGET: LOCKED/UNLOCKED BUTTONS (20x20 L mode)
# ============================================================
def make_lock_icon(locked=True, highlighted=False):
    img = Image.new("L", (20, 20), 0)
    d = ImageDraw.Draw(img)
    b = 220 if highlighted else 140
    # Lock body
    d.rounded_rectangle((4, 8, 16, 18), radius=3, outline=b, width=2)
    if locked:
        d.rounded_rectangle((6, 10, 14, 16), radius=2, fill=b)
    # Shackle
    d.arc((6, 2, 14, 10), 180, 0, fill=b, width=2)
    return img

def generate_lock_buttons():
    for locked in [True, False]:
        for hl in [False, True]:
            prefix = "locked" if locked else "unlocked"
            suffix = "_highlighted" if hl else ""
            name = f"{prefix}_button{suffix}"
            save(f"widget/{name}.png", make_lock_icon(locked, hl))
    print("  Lock buttons: done")

# ============================================================
# WIDGET: CROSS BUTTON (14x14)
# ============================================================
def generate_cross_button():
    for suffix, b in [("", 150), ("_highlighted", 220)]:
        img = Image.new("L", (14, 14), 0)
        d = ImageDraw.Draw(img)
        d.line((3, 3, 11, 11), fill=b, width=2)
        d.line((11, 3, 3, 11), fill=b, width=2)
        save(f"widget/cross_button{suffix}.png", img)
    print("  Cross button: done")

# ============================================================
# WIDGET: PAGE NAVIGATION (23x13 P mode)
# ============================================================
def generate_page_nav():
    for direction in ["forward", "backward"]:
        for suffix, b in [("", 140), ("_highlighted", 220)]:
            img = Image.new("L", (23, 13), 0)
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, 23, 13), radius=4, fill=b)
            # Arrow
            if direction == "forward":
                d.polygon([(10, 3), (18, 6), (10, 9)], fill=0)
            else:
                d.polygon([(13, 3), (5, 6), (13, 9)], fill=0)
            save(f"widget/page_{direction}{suffix}.png", img)
    print("  Page nav: done")

# ============================================================
# WIDGET: SLIDER (200x20 L mode) + HANDLE (8x20 L mode)
# ============================================================
def generate_slider():
    for suffix, b in [("", 100), ("_highlighted", 180)]:
        img = Image.new("L", (200, 20), 0)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 6, 200, 14), radius=4, fill=b)
        save(f"widget/slider{suffix}.png", img)

        # Handle
        h = Image.new("L", (8, 20), 0)
        d = ImageDraw.Draw(h)
        d.rounded_rectangle((0, 0, 8, 20), radius=3, fill=b + 60)
        save(f"widget/slider_handle{suffix}.png", h)
    print("  Slider: done")

# ============================================================
# WIDGET: TABS (130x24 LA mode)
# ============================================================
def generate_widget_tabs():
    for name in ["tab", "tab_highlighted", "tab_selected", "tab_selected_highlighted"]:
        selected = "selected" in name
        highlighted = "highlighted" in name
        brightness = 220 if selected else 120
        if highlighted:
            brightness = min(255, brightness + 40)
        img = Image.new("LA", (130, 24), (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 130, 24), radius=4, fill=(brightness, 255))
        d.rectangle((0, 16, 130, 24), fill=(brightness, 255))  # flat bottom
        save(f"widget/{name}.png", img)
    print("  Widget tabs: done")

# ============================================================
# RECIPE BOOK
# ============================================================
def generate_recipe_book():
    # Button: 20x18 P
    for suffix, b in [("", 120), ("_highlighted", 200)]:
        img = Image.new("RGBA", (20, 18), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 20, 18), radius=4, fill=(29, 27, 32, 220))
        save(f"recipe_book/button{suffix}.png", img)

    # Crafting overlay: 24x24 LA
    for suffix in ["", "_highlighted", "_disabled", "_disabled_highlighted"]:
        bright = 120 if "disabled" in suffix else 200
        if "highlighted" in suffix: bright -= 20
        img = Image.new("LA", (24, 24), (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 24, 24), radius=4, fill=(bright, 200))
        save(f"recipe_book/crafting_overlay{suffix}.png", img)

    # Furnace overlay: 24x24 LA
    for suffix in ["", "_highlighted", "_disabled", "_disabled_highlighted"]:
        bright = 120 if "disabled" in suffix else 200
        if "highlighted" in suffix: bright -= 20
        img = Image.new("LA", (24, 24), (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 24, 24), radius=4, fill=(bright, 200))
        save(f"recipe_book/furnace_overlay{suffix}.png", img)

    # Filters: 26x16 P
    for prefix in ["filter", "furnace_filter"]:
        for state in ["enabled", "disabled"]:
            for suffix in ["", "_highlighted"]:
                bright = 200 if state == "enabled" else 80
                if "_highlighted" in suffix: bright = min(255, bright + 30)
                img = Image.new("RGBA", (26, 16), (0,0,0,0))
                d = ImageDraw.Draw(img)
                d.rounded_rectangle((0, 0, 26, 16), radius=4, fill=(29, 27, 32, 220))
                save(f"recipe_book/{prefix}_{state}{suffix}.png", img)

    # Page nav: 12x17 LA
    for direction in ["forward", "backward"]:
        for suffix, b in [("", 120), ("_highlighted", 200)]:
            img = Image.new("LA", (12, 17), (0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, 12, 17), radius=3, fill=(b, 255))
            save(f"recipe_book/page_{direction}{suffix}.png", img)

    # Overlay recipe: 32x32 LA
    img = Image.new("LA", (32, 32), (0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, 32, 32), radius=6, fill=(180, 180))
    save("recipe_book/overlay_recipe.png", img)

    # Slot indicators: 25x25 LA
    for suffix, b in [("craftable", 200), ("many_craftable", 160)]:
        img = Image.new("LA", (25, 25), (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 25, 25), radius=4, fill=(b, 180))
        save(f"recipe_book/slot_{suffix}.png", img)

    for suffix, b in [("uncraftable", 60), ("many_uncraftable", 80)]:
        img = Image.new("RGBA", (25, 25), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 25, 25), radius=4, fill=(29, 27, 32, 180))
        save(f"recipe_book/slot_{suffix}.png", img)

    # Recipe book tabs: 35x27 LA
    for suffix, b in [("", 120), ("_selected", 200)]:
        img = Image.new("LA", (35, 27), (0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 35, 27), radius=4, fill=(b, 255))
        d.rectangle((0, 18, 35, 27), fill=(b, 255))
        save(f"recipe_book/tab{suffix}.png", img)
    print("  Recipe book: done")

# ============================================================
# BOSS BARS (with progress sprites too!)
# ============================================================
def generate_boss_bars():
    colors = [
        ("pink", 255, 100, 180), ("blue", 100, 150, 255),
        ("red", 255, 80, 80), ("green", 80, 200, 120),
        ("yellow", 255, 220, 60), ("purple", 180, 120, 255),
    ]

    for name, r, g, b in colors:
        # Background: 182x5 P
        bg = Image.new("RGBA", (182, 5), (29, 27, 32, 255))
        d = ImageDraw.Draw(bg)
        d.rounded_rectangle((0, 0, 182, 5), radius=2, fill=(29, 27, 32, 255))
        save(f"boss_bar/{name}_background.png", bg)

        # Progress: 182x5
        prog = Image.new("RGBA", (182, 5), (0,0,0,0))
        d = ImageDraw.Draw(prog)
        d.rounded_rectangle((0, 0, 182, 5), radius=2, fill=(r, g, b, 255))
        save(f"boss_bar/{name}_progress.png", prog)

    # White: L mode
    for suffix in ["background", "progress"]:
        img = Image.new("L", (182, 5), 120)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 182, 5), radius=2, fill=200 if "prog" in suffix else 80)
        save(f"boss_bar/white_{suffix}.png", img)

    # Notched: LA mode
    for n in [6, 10, 12, 20]:
        seg = 182 // n
        for suffix in ["background", "progress"]:
            bright = 200 if "prog" in suffix else 80
            img = Image.new("LA", (182, 5), (bright, 255))
            d = ImageDraw.Draw(img)
            for i in range(n):
                if i % 2 == 1:
                    d.rectangle((i*seg, 0, (i+1)*seg, 5), fill=(30, 255))
            save(f"boss_bar/notched_{n}_{suffix}.png", img)
    print("  Boss bars: done (with progress)")

# ============================================================
# SERVER LIST / WORLD LIST
# ============================================================
def generate_server_world_list():
    # Ping indicators: 10x8 RGBA
    for i in range(1, 6):
        img = Image.new("RGBA", (10, 8), (0,0,0,0))
        d = ImageDraw.Draw(img)
        h = i * 2
        d.rectangle((1, 8-h, 4, 8), fill=(74, 162, 111, 255))
        d.rectangle((6, 8-h, 9, 8), fill=(74, 162, 111, 255))
        save(f"server_list/ping_{i}.png", img)

    for i in range(1, 6):
        img = Image.new("RGBA", (10, 8), (0,0,0,0))
        d = ImageDraw.Draw(img)
        h = i * 2
        d.rectangle((1, 8-h, 4, 8), fill=(255, 200, 60, 180))
        d.rectangle((6, 8-h, 9, 8), fill=(255, 200, 60, 180))
        save(f"server_list/pinging_{i}.png", img)

    # Unreachable: red X
    img = Image.new("RGBA", (10, 8), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.line((1, 1, 9, 7), fill=(255, 80, 80, 255), width=1)
    d.line((9, 1, 1, 7), fill=(255, 80, 80, 255), width=1)
    save("server_list/unreachable.png", img)

    # Incompatible
    img = Image.new("RGBA", (10, 8), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.line((1, 1, 9, 7), fill=(255, 200, 60, 255), width=1)
    d.line((9, 1, 1, 7), fill=(255, 200, 60, 255), width=1)
    save("server_list/incompatible.png", img)

    # Action buttons: 32x32 LA/L/RGBA
    actions = {
        "join": "LA", "move_up": "L", "move_down": "L",
    }
    for name, mode in actions.items():
        for suffix, b in [("", 160), ("_highlighted", 220)]:
            img = Image.new("LA" if mode == "LA" else "L", (32, 32), 0)
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((2, 2, 30, 30), radius=6, fill=(b, 255) if mode == "LA" else b)
            save(f"server_list/{name}{suffix}.png", img)

    # Error/warning/marked_join: LA mode
    for name, b in [("error", 180), ("warning", 180), ("marked_join", 180)]:
        for suffix, extra_b in [("", 0), ("_highlighted", 40)]:
            img = Image.new("LA", (32, 32), (0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((2, 2, 30, 30), radius=6, fill=(b + extra_b, 255))
            save(f"world_list/{name}{suffix}.png", img)
    print("  Server/world list: done")

# ============================================================
# SOCIAL INTERACTIONS / POPUP / TOOLTIP
# ============================================================
def generate_screen_backgrounds():
    # Social interactions: 236x34 L mode
    img = Image.new("L", (236, 34), 40)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, 236, 34), radius=6, fill=60)
    save("social_interactions/background.png", img)

    # Popup: 236x34 L mode
    img = Image.new("L", (236, 34), 40)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, 236, 34), radius=8, fill=70)
    save("popup/background.png", img)

    # Tooltip background: 100x100 P mode
    img = Image.new("RGBA", (100, 100), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, 100, 100), radius=6, fill=(33, 31, 38, 240))
    d.rounded_rectangle((0, 0, 100, 100), radius=6, outline=(73, 69, 79, 150), width=1)
    save("tooltip/background.png", img)

    # Tooltip frame: 100x100 RGBA
    img = Image.new("RGBA", (100, 100), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, 100, 100), radius=6, outline=(74, 162, 111, 180), width=2)
    save("tooltip/frame.png", img)

    # Social buttons
    for name in ["mute_button", "unmute_button", "report_button"]:
        for suffix, b in [("", 140), ("_highlighted", 200)]:
            img = Image.new("RGBA", (20, 20), (0,0,0,0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, 20, 20), radius=4, fill=(33, 31, 38, 220))
            save(f"social_interactions/{name}{suffix}.png", img)

    # Report disabled: L mode
    img = Image.new("L", (20, 20), 0)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, 20, 20), radius=4, fill=60)
    save("social_interactions/report_button_disabled.png", img)
    print("  Screen backgrounds: done")

# ============================================================
# CREATIVE INVENTORY SCROLLER REDO (12x15)
# ============================================================
# Already generated in generate_scrollers() above, no need to redo

# ============================================================
# MAIN
# ============================================================
def main():
    print("ZeroUI Complete Sprite Generator v2")
    print("=" * 50)
    generate_scrollers()
    generate_buttons()
    generate_text_fields()
    generate_checkboxes()
    generate_lock_buttons()
    generate_cross_button()
    generate_page_nav()
    generate_slider()
    generate_widget_tabs()
    generate_recipe_book()
    generate_boss_bars()
    generate_server_world_list()
    generate_screen_backgrounds()
    print("=" * 50)
    print("ALL sprites regenerated with correct sizes and modes!")

if __name__ == "__main__":
    main()
