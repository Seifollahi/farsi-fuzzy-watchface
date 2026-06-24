from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

width, height = 144, 168

font_path = "resources/fonts/Vazirmatn-Black.ttf"
font_small = ImageFont.truetype(font_path, 22)
font_large = ImageFont.truetype(font_path, 38)

def shape(text):
    reshaper = arabic_reshaper.ArabicReshaper(configuration={
        'delete_harakat': True,
        'support_ligatures': True,
    })
    return get_display(reshaper.reshape(text))

def draw_right_aligned(draw, text, font, y, margin=8):
    """Draw text right-aligned, returns the bounding box height."""
    shaped = shape(text)
    bb = draw.textbbox((0, 0), shaped, font=font)
    w = bb[2] - bb[0]
    h = bb[3] - bb[1]
    x = width - w - margin
    if x < 0: x = 0
    draw.text((x, y), shaped, font=font, fill=0)
    return h

img = Image.new("L", (width, height), color=255)
draw = ImageDraw.Draw(img)

# Line 1 (small, right-aligned): الان تقریبا
draw_right_aligned(draw, "الان تقریبا", font_small, 8)

# Line 2 (small, right-aligned): ساعت
draw_right_aligned(draw, "ساعت", font_small, 38)

# Line 3 (large, right-aligned): ده و ربعه
# Check if it fits in one line, otherwise split
test_text = shape("ده و ربعه")
bb = draw.textbbox((0, 0), test_text, font=font_large)
text_w = bb[2] - bb[0]

if text_w <= width - 16:
    # Fits on one line
    draw_right_aligned(draw, "ده و ربعه", font_large, 68)
else:
    # Split into two lines
    draw_right_aligned(draw, "ده و", font_large, 68)
    draw_right_aligned(draw, "ربعه", font_large, 115)

img.save("test_v4.png")
print("Saved test_v4.png")
