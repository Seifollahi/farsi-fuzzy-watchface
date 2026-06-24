from PIL import Image, ImageDraw, ImageFont
import os
import json
import arabic_reshaper
from bidi.algorithm import get_display

hours_farsi = [
    "دوازده", "یک", "دو", "سه", "چهار", "پنج", 
    "شش", "هفت", "هشت", "نه", "ده", "یازده"
]
next_hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]

os.makedirs("resources/images", exist_ok=True)

width, height = 144, 168

font_path = "resources/fonts/Vazirmatn-Black.ttf"
try:
    font_small = ImageFont.truetype(font_path, 22)
    font_large = ImageFont.truetype(font_path, 38)
except IOError:
    print("Font not found.")
    exit(1)

def shape(text):
    reshaper = arabic_reshaper.ArabicReshaper(configuration={
        'delete_harakat': True,
        'support_ligatures': True,
    })
    return get_display(reshaper.reshape(text))

def draw_right_aligned(draw, text, font, y, margin=8):
    """Draw text right-aligned, returns bounding box height."""
    shaped = shape(text)
    bb = draw.textbbox((0, 0), shaped, font=font)
    w = bb[2] - bb[0]
    h = bb[3] - bb[1]
    x = width - w - margin
    if x < 0: x = 0
    draw.text((x, y), shaped, font=font, fill=255)
    return h

def draw_large_auto_wrap(draw, text, font, start_y, margin=8):
    """Draw large text right-aligned, auto-wrapping if too wide."""
    shaped = shape(text)
    bb = draw.textbbox((0, 0), shaped, font=font)
    text_w = bb[2] - bb[0]
    
    if text_w <= width - margin * 2:
        # Fits on one line
        draw_right_aligned(draw, text, font, start_y, margin)
    else:
        # Split into words and distribute across lines
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = " ".join(current_line + [word])
            test_shaped = shape(test_line)
            bb = draw.textbbox((0, 0), test_shaped, font=font)
            if bb[2] - bb[0] <= width - margin * 2:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        
        y = start_y
        for line in lines:
            draw_right_aligned(draw, line, font, y, margin)
            y += 47  # line spacing for 38pt font

def create_image(filename, ftype, hour_str="", mod_str=""):
    img = Image.new('L', (width, height), color=0)
    draw = ImageDraw.Draw(img)
    
    if ftype in ["exact", "half", "quarter"]:
        # Line 1 (small): الان تقریبا
        draw_right_aligned(draw, "الان تقریبا", font_small, 8)
        # Line 2 (small): ساعت
        draw_right_aligned(draw, "ساعت", font_small, 38)
        
        if ftype == "exact":
            # Large: just the hour + ه suffix
            draw_large_auto_wrap(draw, hour_str + "ه", font_large, 68)
        elif ftype == "half":
            # Large: hour و نیمه
            draw_large_auto_wrap(draw, hour_str + " و نیمه", font_large, 68)
        elif ftype == "quarter":
            # Large: hour و ربعه
            draw_large_auto_wrap(draw, hour_str + " و ربعه", font_large, 68)

    elif ftype == "tonext":
        # Line 1 (small): الان تقریبا
        draw_right_aligned(draw, "الان تقریبا", font_small, 8)
        # Large: یه ربع به hour
        draw_large_auto_wrap(draw, "یه ربع به " + hour_str, font_large, 48)
        
    elif ftype == "single":
        # Line 1 (small): الان تقریبا
        draw_right_aligned(draw, "الان تقریبا", font_small, 8)
        # Large: single word centered
        draw_large_auto_wrap(draw, hour_str, font_large, 68)

    img.save(filename)

resources = []
c_header_lines = [
    '#pragma once',
    '#include <pebble.h>',
    '#define ACCURACY_QUARTER    0',
    '#define ACCURACY_HALF       1',
    '#define ACCURACY_HOUR       2',
    '#define ACCURACY_HALF_DAY   3',
    '#define ACCURACY_DAY_NIGHT  4',
    '#define ACCURACY_PERIOD     5',
    ''
]

def add_res(name, ftype, hour_str="", mod_str=""):
    filename = f"resources/images/{name.lower()}.png"
    create_image(filename, ftype, hour_str, mod_str)
    resources.append({"type": "bitmap", "name": name, "file": f"images/{name.lower()}.png"})
    return f"RESOURCE_ID_{name}"

exact_ids = []
quarter_ids = []
half_ids = []
to_next_ids = []

for i in range(12):
    exact_ids.append(add_res(f"IMG_EXACT_{i}", "exact", hours_farsi[i]))
    quarter_ids.append(add_res(f"IMG_QUARTER_{i}", "quarter", hours_farsi[i]))
    half_ids.append(add_res(f"IMG_HALF_{i}", "half", hours_farsi[i]))
    to_next_ids.append(add_res(f"IMG_TONEXT_{i}", "tonext", hours_farsi[next_hours[i]]))

half_day_ids = [add_res("IMG_HALFDAY_0", "single", "صبحه"), add_res("IMG_HALFDAY_1", "single", "شبه")]
day_night_ids = [add_res("IMG_DAYNIGHT_0", "single", "روزه"), add_res("IMG_DAYNIGHT_1", "single", "شبه")]
period_ids = [
    add_res("IMG_PERIOD_0", "single", "صبحه"),
    add_res("IMG_PERIOD_1", "single", "ظهره"),
    add_res("IMG_PERIOD_2", "single", "بعدازظهره"),
    add_res("IMG_PERIOD_3", "single", "عصره"),
    add_res("IMG_PERIOD_4", "single", "شبه")
]

c_header_lines.append('static const uint32_t FARSI_QUARTER[12][4] = {')
for i in range(12): c_header_lines.append(f'  {{ {exact_ids[i]}, {quarter_ids[i]}, {half_ids[i]}, {to_next_ids[i]} }},')
c_header_lines.append('};')

c_header_lines.append('static const uint32_t FARSI_HALF[12][2] = {')
for i in range(12): c_header_lines.append(f'  {{ {exact_ids[i]}, {half_ids[i]} }},')
c_header_lines.append('};')

c_header_lines.append('static const uint32_t FARSI_HOUR[12] = {')
for i in range(12): c_header_lines.append(f'  {exact_ids[i]},')
c_header_lines.append('};')

c_header_lines.append('static const uint32_t FARSI_HALF_DAY[2] = {')
for x in half_day_ids: c_header_lines.append(f'  {x},')
c_header_lines.append('};')

c_header_lines.append('static const uint32_t FARSI_DAY_NIGHT[2] = {')
for x in day_night_ids: c_header_lines.append(f'  {x},')
c_header_lines.append('};')

c_header_lines.append('static const uint32_t FARSI_PERIOD[5] = {')
for x in period_ids: c_header_lines.append(f'  {x},')
c_header_lines.append('};')

with open('src/c/farsi_bitmaps.h', 'w') as f:
    f.write('\n'.join(c_header_lines))

with open('package.json', 'r') as f:
    data = json.load(f)

data['pebble']['resources']['media'] = resources

with open('package.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Generated {len(resources)} bitmaps with new multi-size layout!")
