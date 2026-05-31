"""
Generate extension icons (PNG) programmatically using Pillow.
Run once: python extension/assets/icons/generate_icons.py

Requires: pip install Pillow
"""
from pathlib import Path

SIZES = [16, 48, 128]
OUT_DIR = Path(__file__).parent


def generate_icon(size: int) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed. Run: pip install Pillow")
        return

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle — blue
    margin = size // 8
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=(59, 91, 219, 255),
    )

    # Shield shape
    sw = int(size * 0.45)
    sh = int(size * 0.55)
    sx = (size - sw) // 2
    sy = int(size * 0.22)
    shield_pts = [
        (sx + sw // 2, sy),
        (sx + sw, sy + sh // 3),
        (sx + sw, sy + sh * 2 // 3),
        (sx + sw // 2, sy + sh),
        (sx, sy + sh * 2 // 3),
        (sx, sy + sh // 3),
    ]
    draw.polygon(shield_pts, fill=(255, 255, 255, 230))

    # "A" letter in shield
    if size >= 48:
        font_size = max(size // 4, 8)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
        draw.text(
            (size // 2, size // 2),
            "A",
            fill=(59, 91, 219, 255),
            font=font,
            anchor="mm",
        )

    out_path = OUT_DIR / f"icon{size}.png"
    img.save(out_path, "PNG")
    print(f"Generated {out_path}")


if __name__ == "__main__":
    for s in SIZES:
        generate_icon(s)
    print("Done. Place these PNG files in extension/assets/icons/")
