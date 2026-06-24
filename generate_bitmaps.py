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
bg_color, text_color = (0,0,0), (255,255,255)

font_path = "resources/fonts/Vazirmatn-Black.ttf"
try:
    font_header = ImageFont.truetype(font_path, 20)
    font_saat = ImageFont.truetype(font_path, 54)
    font_hour = ImageFont.truetype(font_path, 48)
    font_mod = ImageFont.truetype(font_path, 56)
    font_conn = ImageFont.truetype(font_path, 22)
    font_huge = ImageFont.truetype(font_path, 60)
    font_med = ImageFont.truetype(font_path, 36)
except IOError:
    print("Font not found.")
    exit(1)

def shape(text):
    configuration = {
        'delete_harakat': True,
        'support_ligatures': True,
    }
    reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)
    return get_display(reshaper.reshape(text))

def draw_header(draw):
    h_text = shape("الان تقریبا")
    hb = draw.textbbox((0, 0), h_text, font=font_header)
    draw.text((width - (hb[2]-hb[0]) - 5, -5), h_text, font=font_header, fill=text_color)

def create_image(filename, ftype, hour_str="", mod_str=""):
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    
    if ftype in ["exact", "half", "quarter"]:
        # 1. "ساعت"
        saat_text = shape("ساعت")
        sb = draw.textbbox((0, 0), saat_text, font=font_saat)
        saat_w = sb[2]-sb[0]
        saat_x = width - saat_w - 5
        saat_y = 20
        draw.text((saat_x, saat_y), saat_text, font=font_saat, fill=text_color)
        
        # 2. Hour
        hour_text = shape(hour_str)
        hob = draw.textbbox((0, 0), hour_text, font=font_hour)
        hour_w = hob[2]-hob[0]
        hour_x = width - hour_w - 5
        hour_y = saat_y + 40
        
        if ftype == "exact":
            # Just shift hour down to be centered in bottom space
            hour_x = width - hour_w - 20
            hour_y = saat_y + 60
            draw.text((hour_x, hour_y), hour_text, font=font_huge, fill=text_color)
        else:
            # Shift slightly right if it's quarter/half to leave room
            draw.text((hour_x, hour_y), hour_text, font=font_hour, fill=text_color)
            
            # 3. Modifier (نیم or ربع)
            mod_text = shape(mod_str)
            mb = draw.textbbox((0, 0), mod_text, font=font_mod)
            mod_w = mb[2]-mb[0]
            mod_x = hour_x - mod_w - 2
            if mod_x < 0: mod_x = 0 # Prevent clipping
            mod_y = saat_y + 35
            draw.text((mod_x, mod_y), mod_text, font=font_mod, fill=text_color)
            
            # 4. Connector "و"
            conn_text = shape("و")
            conn_x = mod_x + (10 if mod_str == "نیم" else 25)
            conn_y = mod_y - (8 if mod_str == "نیم" else 0)
            draw.text((conn_x, conn_y), conn_text, font=font_conn, fill=text_color)

    elif ftype == "tonext":
        t1 = shape("یه ربع")
        b1 = draw.textbbox((0,0), t1, font=font_med)
        draw.text((width - (b1[2]-b1[0]) - 10, 25), t1, font=font_med, fill=text_color)
        
        t2 = shape("مونده به")
        b2 = draw.textbbox((0,0), t2, font=font_med)
        draw.text((width - (b2[2]-b2[0]) - 20, 65), t2, font=font_med, fill=text_color)
        
        t3 = shape(hour_str)
        b3 = draw.textbbox((0,0), t3, font=font_huge)
        draw.text((width - (b3[2]-b3[0]) - 5, 105), t3, font=font_huge, fill=text_color)
        
    elif ftype == "single":
        t1 = shape(hour_str)
        b1 = draw.textbbox((0,0), t1, font=font_huge)
        w1 = b1[2]-b1[0]
        h1 = b1[3]-b1[1]
        draw.text(((width - w1)//2, 40 + (128-h1)//2), t1, font=font_huge, fill=text_color)

    img = img.convert('L')
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
    quarter_ids.append(add_res(f"IMG_QUARTER_{i}", "quarter", hours_farsi[i], "ربع"))
    half_ids.append(add_res(f"IMG_HALF_{i}", "half", hours_farsi[i], "نیم"))
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

print("Generated full interwoven bitmaps!")
