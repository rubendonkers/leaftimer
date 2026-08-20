"""
Procedural asset and icon generator for the Nature Shutdown Timer.
Generates botanical leaf icons and app .ico files automatically.
"""

import os
from PIL import Image, ImageDraw

import sys

def get_asset_path(filename: str) -> str:
    """Returns absolute path to an asset in the assets directory."""
    if hasattr(sys, "_MEIPASS"):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    return os.path.join(assets_dir, filename)

def generate_leaf_icon(size: int = 256) -> Image.Image:
    """
    Generates a minimalist, modern botanical leaf emblem with high resolution antialiasing.
    """
    scale = 4  # Supersample for smooth curves
    w, h = size * scale, size * scale
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Soft rounded organic background circle/badge
    pad = int(16 * scale)
    badge_bounds = [pad, pad, w - pad, h - pad]
    draw.ellipse(badge_bounds, fill=(35, 75, 52, 255))

    # Inner soft gradient / leaf contour
    # Draw leaf body using bezier-like polygon points
    cx, cy = w // 2, h // 2
    leaf_points = [
        (cx, cy - int(65 * scale)),               # Leaf tip (top)
        (cx + int(48 * scale), cy - int(25 * scale)), # Upper right curve
        (cx + int(52 * scale), cy + int(20 * scale)), # Lower right curve
        (cx + int(10 * scale), cy + int(65 * scale)), # Stem base
        (cx, cy + int(60 * scale)),               # Base indent
        (cx - int(45 * scale), cy + int(25 * scale)), # Lower left curve
        (cx - int(48 * scale), cy - int(25 * scale)), # Upper left curve
    ]
    draw.polygon(leaf_points, fill=(110, 207, 142, 255))

    # Leaf center vein line
    draw.line(
        [(cx, cy - int(58 * scale)), (cx + int(5 * scale), cy + int(58 * scale))],
        fill=(35, 75, 52, 220),
        width=int(4 * scale)
    )
    
    # Subtle secondary leaf branching
    draw.line(
        [(cx, cy - int(20 * scale)), (cx + int(28 * scale), cy - int(32 * scale))],
        fill=(35, 75, 52, 200),
        width=int(3 * scale)
    )
    draw.line(
        [(cx, cy + int(5 * scale)), (cx - int(25 * scale), cy - int(5 * scale))],
        fill=(35, 75, 52, 200),
        width=int(3 * scale)
    )

    # Downsample with Lanczos for anti-aliasing
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

def ensure_assets():
    """Generates and saves icon files (.png and .ico) if they don't already exist."""
    icon_png_path = get_asset_path("app_icon.png")
    icon_ico_path = get_asset_path("app_icon.ico")

    img = generate_leaf_icon(256)
    img.save(icon_png_path, format="PNG")
    
    # Save multi-size .ico file for Windows
    img.save(
        icon_ico_path,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    )
    return icon_png_path, icon_ico_path

if __name__ == "__main__":
    png, ico = ensure_assets()
    print(f"Generated assets:\n - {png}\n - {ico}")
