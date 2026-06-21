#!/usr/bin/env python3
"""
ZeroUI HD Regenerator
2x resolution containers, anti-aliased everything, same light theme
"""

from PIL import Image, ImageDraw, ImageFilter
import zipfile, io, os, json

z = zipfile.ZipFile('/Users/cangcang/Library/Application Support/minecraft/versions/1.21.11/1.21.11.jar')

# Warm light palette (unchanged)
LIGHT = (180, 175, 185)
MED   = (160, 155, 165)
DARK  = (130, 125, 135)
WHITE = (210, 208, 215)
ACCENT = (74, 162, 111)

BASE = os.path.join(os.path.dirname(__file__) or ".", "assets", "minecraft", "textures", "gui")


def save(path, img):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    img.save(full)


def recolor_vanilla(data, scale=1, smooth=True):
    """Extract vanilla, recolor, optionally upscale."""
    vanilla = Image.open(io.BytesIO(data)).convert('RGBA')
    w, h = vanilla.size

    if scale > 1:
        new = Image.new('RGBA', (w * scale, h * scale), (0, 0, 0, 0))
    else:
        new = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    vp = vanilla.load()

    if scale > 1:
        # Upscale using NEAREST first for pixel art, then smooth
        upscaled = vanilla.resize((w * scale, h * scale), Image.NEAREST)
        upscaled_rgba = upscaled.convert('RGBA')
        up = upscaled_rgba.load()
        nd = new.load()

        for y in range(h * scale):
            for x in range(w * scale):
                r, g, b, a = up[x, y]
                if a < 30:
                    nd[x, y] = (0, 0, 0, 0)
                    continue
                bright = (r + g + b) // 3
                if bright < 30:
                    nd[x, y] = DARK + (a,)
                elif bright < 80:
                    nd[x, y] = MED + (a,)
                elif bright < 150:
                    nd[x, y] = LIGHT + (a,)
                else:
                    nd[x, y] = WHITE + (a,)

        if smooth:
            new = new.filter(ImageFilter.SMOOTH_MORE)
    else:
        nd = new.load()
        for y in range(h):
            for x in range(w):
                r, g, b, a = vp[x, y]
                if a < 30:
                    nd[x, y] = (0, 0, 0, 0)
                    continue
                bright = (r + g + b) // 3
                if bright < 30:
                    nd[x, y] = DARK + (a,)
                elif bright < 80:
                    nd[x, y] = MED + (a,)
                elif bright < 150:
                    nd[x, y] = LIGHT + (a,)
                else:
                    nd[x, y] = WHITE + (a,)

    return new


# ===== 1. CONTAINERS: 512x512 (2x HD) =====
print("Containers (512x512 HD)...")
containers = ['inventory', 'crafting_table', 'furnace', 'generic_54',
              'dispenser', 'hopper', 'enchanting_table', 'anvil', 'beacon',
              'smithing', 'loom', 'stonecutter', 'grindstone', 'cartography_table',
              'shulker_box', 'blast_furnace', 'smoker', 'brewing_stand']

for name in containers:
    try:
        data = z.read(f'assets/minecraft/textures/gui/container/{name}.png')
        new = recolor_vanilla(data, scale=2, smooth=True)
        # Add subtle border accent
        d = ImageDraw.Draw(new)
        d.rectangle((0, 0, new.width, 8), fill=ACCENT + (180,))
        save(f'container/{name}.png', new)
    except Exception as e:
        print(f'  SKIP {name}: {e}')

for fn in ['blast_furnace', 'smoker']:
    try:
        img = Image.open(os.path.join(BASE, 'container/furnace.png'))
        img.save(os.path.join(BASE, f'container/{fn}.png'))
    except:
        pass

print("  done")

# ===== 2. Creative inventory tab pages: 512x512 =====
print("Creative tab pages (512x512)...")
for name in ['tab_inventory', 'tab_items', 'tab_item_search']:
    try:
        data = z.read(f'assets/minecraft/textures/gui/container/creative_inventory/{name}.png')
        new = recolor_vanilla(data, scale=2, smooth=True)
        save(f'container/creative_inventory/{name}.png', new)
    except Exception as e:
        print(f'  SKIP {name}: {e}')
print("  done")

# ===== 3. Recipe book bg: 512x512 =====
print("Recipe book (512x512)...")
try:
    data = z.read('assets/minecraft/textures/gui/recipe_book.png')
    new = recolor_vanilla(data, scale=2, smooth=True)
    save('recipe_book.png', new)
except Exception as e:
    print(f'  SKIP: {e}')
print("  done")

# ===== 4. Options background: 512x512 =====
print("Options bg (512x512)...")
try:
    data = z.read('assets/minecraft/textures/gui/options_background.png')
    new = recolor_vanilla(data, scale=2, smooth=True)
    d = ImageDraw.Draw(new)
    d.rectangle((0, 0, new.width, 10), fill=ACCENT + (160,))
    save('options_background.png', new)
except:
    pass
print("  done")

# ===== 5. Book: 512x512 =====
try:
    data = z.read('assets/minecraft/textures/gui/book.png')
    new = recolor_vanilla(data, scale=2, smooth=True)
    save('book.png', new)
except:
    pass

# ===== 6. All sprites: keep size, but smooth =====
print("Sprites (anti-aliased)...")
count = 0
for name in z.namelist():
    if not name.startswith('assets/minecraft/textures/gui/sprites/') or not name.endswith('.png'):
        continue
    rel = name.replace('assets/minecraft/textures/gui/sprites/', '')
    data = z.read(name)
    vanilla = Image.open(io.BytesIO(data))

    # Small sprites: recolor at same size, no scale
    new = recolor_vanilla(data, scale=1, smooth=False)

    # For very small sprites (9x9 hearts, etc.), keep pixel-perfect
    if vanilla.width <= 32 and vanilla.height <= 32:
        new = new.filter(ImageFilter.SMOOTH)

    save(f'sprites/{rel}', new)
    count += 1

print(f"  {count} sprites")

# ===== 7. Creative tabs: fix accent positions =====
print("Creative tabs accent fix...")
for i in range(1, 8):
    for top in [True, False]:
        for sel in [True, False]:
            v = 'top' if top else 'bottom'
            s = 'selected' if sel else 'unselected'
            path = f'sprites/container/creative_inventory/tab_{v}_{s}_{i}.png'
            full = os.path.join(BASE, path)
            if not os.path.exists(full):
                continue
            img = Image.open(full).convert('RGBA')
            if sel:
                d = ImageDraw.Draw(img)
                if top:
                    for y in range(0, 4):
                        for x in range(img.width):
                            if img.getpixel((x, y))[3] > 30:
                                img.putpixel((x, y), ACCENT + (255,))
                else:
                    for y in range(max(0, img.height - 4), img.height):
                        for x in range(img.width):
                            if img.getpixel((x, y))[3] > 30:
                                img.putpixel((x, y), ACCENT + (255,))
            img.save(full)
print("  done")

# ===== 8. Buttons HD =====
print("Buttons HD...")
WIDGET = os.path.join(BASE, 'sprites', 'widget')
os.makedirs(WIDGET, exist_ok=True)

btns = {
    'button.png': LIGHT + (240,),
    'button_disabled.png': DARK + (160,),
    'button_highlighted.png': ACCENT + (220,),
}
for name, fill in btns.items():
    img = Image.new('RGBA', (200, 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 200, 20), fill=fill)
    # Subtle bottom edge
    edge = tuple(max(0, c - 20) for c in fill[:3]) + (fill[3] // 2,)
    d.rectangle((0, 18, 200, 20), fill=edge)
    img.save(os.path.join(WIDGET, name))

with open(os.path.join(WIDGET, 'button.png.mcmeta'), 'w') as f:
    json.dump({"gui": {"scaling": {"type": "nine_slice", "width": 200, "height": 20, "border": 3}}}, f)

sliders = {
    'slider.png': (LIGHT + (240,), 200, 20),
    'slider_highlighted.png': (ACCENT + (200,), 200, 20),
    'slider_handle.png': (MED + (255,), 8, 20),
    'slider_handle_highlighted.png': (ACCENT + (240,), 8, 20),
}
for name, (fill, w, h) in sliders.items():
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, w, h), fill=fill)
    img.save(os.path.join(WIDGET, name))
print("  done")

# ===== 9. Hearts, food, armor with pixel-perfect shapes, better colors =====
print("Hearts & icons...")
HEART = os.path.join(BASE, 'sprites', 'hud', 'heart')
os.makedirs(HEART, exist_ok=True)

vf = Image.open(io.BytesIO(z.read('assets/minecraft/textures/gui/sprites/hud/heart/full.png'))).convert('RGBA')
vc = Image.open(io.BytesIO(z.read('assets/minecraft/textures/gui/sprites/hud/heart/container.png')))

states = [
    ('container', (200, 200, 200)), ('container_blinking', (200, 200, 200)),
    ('container_hardcore', (255, 200, 60)), ('container_hardcore_blinking', (255, 200, 60)),
    ('vehicle_container', (255, 200, 100)),
    ('full', (255, 65, 75)), ('full_blinking', (255, 65, 75)),
    ('half', (255, 65, 75)), ('half_blinking', (255, 65, 75)),
    ('hardcore_full', (255, 140, 50)), ('hardcore_half', (255, 140, 50)),
    ('hardcore_full_blinking', (255, 140, 50)), ('hardcore_half_blinking', (255, 140, 50)),
    ('absorbing_full', (255, 210, 50)), ('absorbing_half', (255, 210, 50)),
    ('absorbing_full_blinking', (255, 210, 50)), ('absorbing_half_blinking', (255, 210, 50)),
    ('poisoned_full', (130, 200, 60)), ('poisoned_half', (130, 200, 60)),
    ('poisoned_full_blinking', (130, 200, 60)), ('poisoned_half_blinking', (130, 200, 60)),
    ('frozen_full', (80, 175, 255)), ('frozen_half', (80, 175, 255)),
    ('frozen_full_blinking', (80, 175, 255)), ('frozen_half_blinking', (80, 175, 255)),
    ('withered_full', (60, 60, 60)), ('withered_half', (60, 60, 60)),
    ('withered_full_blinking', (60, 60, 60)), ('withered_half_blinking', (60, 60, 60)),
    ('vehicle_full', (255, 210, 80)), ('vehicle_half', (255, 210, 80)),
]

for name, color in states:
    is_half = 'half' in name
    is_container = 'container' in name
    src = vc.convert('RGBA') if is_container else vf
    new = Image.new('RGBA', (9, 9), (0, 0, 0, 0))
    sp = src.load(); nd = new.load()
    for y in range(9):
        for x in range(9):
            r, g, b, a = sp[x, y]
            if a > 50:
                nd[x, y] = color + (a,)
    if is_half and not is_container:
        for y in range(9):
            for x in range(5, 9):
                px = new.getpixel((x, y))
                if px[3] > 50:
                    new.putpixel((x, y), (px[0] // 4, px[1] // 4, px[2] // 4, px[3]))
    new.save(os.path.join(HEART, f'{name}.png'))

# Food
FOOD = os.path.join(BASE, 'sprites', 'hud')
vf2 = Image.open(io.BytesIO(z.read('assets/minecraft/textures/gui/sprites/hud/food_full.png'))).convert('RGBA')
for name, color in [('food_full', (255, 155, 60)), ('food_full_hunger', (180, 190, 100)),
                     ('food_half', (255, 155, 60)), ('food_half_hunger', (180, 190, 100))]:
    new = Image.new('RGBA', (9, 9), (0, 0, 0, 0))
    sp = vf2.load(); nd = new.load()
    for y in range(9):
        for x in range(9):
            r, g, b, a = sp[x, y]
            if a > 50:
                nd[x, y] = color + (a,)
    if 'half' in name:
        for y in range(9):
            for x in range(5, 9):
                px = new.getpixel((x, y))
                if px[3] > 50:
                    new.putpixel((x, y), (px[0] // 4, px[1] // 4, px[2] // 4, px[3]))
    new.save(os.path.join(FOOD, f'{name}.png'))

# Armor
va = Image.open(io.BytesIO(z.read('assets/minecraft/textures/gui/sprites/hud/armor_full.png'))).convert('RGBA')
for name in ['armor_full', 'armor_half']:
    new = Image.new('RGBA', (9, 9), (0, 0, 0, 0))
    sp = va.load(); nd = new.load()
    for y in range(9):
        for x in range(9):
            r, g, b, a = sp[x, y]
            if a > 50:
                nd[x, y] = (180, 195, 230, a)
    if 'half' in name:
        for y in range(9):
            for x in range(5, 9):
                px = new.getpixel((x, y))
                if px[3] > 50:
                    new.putpixel((x, y), (px[0] // 4, px[1] // 4, px[2] // 4, px[3]))
    new.save(os.path.join(FOOD, f'{name}.png'))

print("  done")

# ===== 10. Crosshair: crisp =====
cr = Image.new('LA', (15, 15), (0, 0))
cd = ImageDraw.Draw(cr)
cd.rectangle((7, 0, 7, 5), fill=(220, 255))
cd.rectangle((7, 9, 7, 14), fill=(220, 255))
cd.rectangle((0, 7, 5, 7), fill=(220, 255))
cd.rectangle((9, 7, 14, 7), fill=(220, 255))
cr.save(os.path.join(BASE, 'sprites', 'hud', 'crosshair.png'))

print("\n=== HD regeneration complete ===")
print("Containers: 512x512 (2x HD)")
print(f"Sprites: {count} (anti-aliased)")
