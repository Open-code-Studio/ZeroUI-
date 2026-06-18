#!/usr/bin/env python3
"""
ZeroUI - Multi-Color Variant Generator
Creates separate resource pack variants for each theme color.
Appear as separate entries in Minecraft's resource pack menu.
"""
import os, sys, json
from PIL import Image, ImageDraw

THEMES = {
    "green":   "4AA26F",  # 薄荷绿（当前）
    "blue":    "448AFF",  # 海蓝
    "purple":  "AB47BC",  # 紫色
    "orange":  "FF7043",  # 橘色
    "pink":    "EC407A",  # 粉色
    "teal":    "26A69A",  # 青绿
    "red":     "EF5350",  # 红色
    "amber":   "FFA726",  # 琥珀
}

BASE = os.path.join(os.path.dirname(__file__) or ".")
SRC_ASSETS = os.path.join(BASE, "assets")
RP_BASE = os.path.expanduser("~/Library/Application Support/minecraft/versions/1.21.11/resourcepacks")

def hex_to_rgba(h):
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), 255)

def generate_variant(name, hex_color):
    """Generate a complete ZeroUI variant pack with given color."""
    G = hex_to_rgba(hex_color)
    OUT = (73, 69, 79, 255)
    SC = (29, 27, 32, 255)

    pack_dir = os.path.join(RP_BASE, f"ZeroUI-{name}")
    assets_dir = os.path.join(pack_dir, "assets", "minecraft", "textures", "gui", "sprites")

    # Copy all non-color-specific sprites from base pack
    src_sprites = os.path.join(BASE, "assets", "minecraft", "textures", "gui", "sprites")
    if os.path.exists(pack_dir):
        import shutil
        shutil.rmtree(pack_dir)
    os.makedirs(assets_dir, exist_ok=True)

    # Copy everything first
    import shutil
    shutil.copytree(src_sprites, assets_dir, dirs_exist_ok=True)

    def save(path, img):
        full = os.path.join(assets_dir, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        img.save(full)

    # Override color-specific sprites with the theme color
    # Highlighted button
    img = Image.new("RGBA", (200, 20), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 200, 20), fill=G[:3] + (200,))
    b2 = tuple(min(255, c + 30) for c in G[:3]) + (255,)
    d.rectangle((0, 0, 200, 20), outline=b2, width=2)
    save("widget/button_highlighted.png", img)

    # Slider highlighted
    save("widget/slider_highlighted.png", img)
    img_h = Image.new("RGBA", (8, 20), (0,0,0,0))
    d = ImageDraw.Draw(img_h)
    d.rectangle((0, 0, 8, 20), fill=G[:3] + (200,))
    save("widget/slider_handle_highlighted.png", img_h)

    # Text field highlighted
    img = Image.new("RGBA", (200, 20), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 200, 20), fill=SC)
    d.rectangle((0, 0, 200, 20), outline=G[:3] + (220,), width=2)
    save("widget/text_field_highlighted.png", img)

    # Tooltip frame
    img = Image.new("RGBA", (100, 100), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 100, 100), outline=G[:3] + (180,), width=2)
    save("tooltip/frame.png", img)

    # Tooltip background
    img = Image.new("RGBA", (100, 100), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 100, 100), fill=(33, 31, 38, 240))
    d.rectangle((0, 0, 100, 100), outline=OUT[:3] + (150,), width=1)
    save("tooltip/background.png", img)

    # Copy pack.mcmeta and pack.png
    pack_mcmeta = {
        "pack": {
            "pack_format": 55,
            "supported_formats": [46, 55],
            "description": f"§aZeroUI §8- §f{name.upper()} Theme\n§7Material Design 3 UI"
        }
    }
    with open(os.path.join(pack_dir, "pack.mcmeta"), "w") as f:
        json.dump(pack_mcmeta, f, indent=2)

    # Color the pack icon
    icon = Image.open(os.path.join(BASE, "pack.png")).convert("RGBA")
    # Tint the icon's central area
    d = ImageDraw.Draw(icon)
    d.ellipse((29, 29, 99, 99), fill=G[:3] + (200,))
    d.ellipse((29, 29, 99, 99), outline=tuple(min(255,c+20) for c in G[:3]) + (255,), width=2)
    d.ellipse((34, 34, 94, 94), fill=(33, 31, 38, 255))
    # Z letter in theme color
    d.line([(50,45),(78,45),(78,50),(56,50),(55,76),(78,76),(78,83),(50,83)], fill=G, width=5)
    icon.save(os.path.join(pack_dir, "pack.png"))

    print(f"  {name}: #{hex_color} ✓")


def main():
    print("ZeroUI - Generating color variants...")
    print("=" * 50)

    for name, hex_color in THEMES.items():
        generate_variant(name, hex_color)

    print("=" * 50)
    print(f"Generated {len(THEMES)} color variants in:")
    print(f"  {RP_BASE}/")
    print(f"\nEach appears as 'ZeroUI-<color>' in the resource pack menu.")
    print(f"In-game: Options → Resource Packs → select your color!")


if __name__ == "__main__":
    main()
