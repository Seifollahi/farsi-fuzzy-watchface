from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

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

configuration = {
    'delete_harakat': True,
    'support_ligatures': True,
}
reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)

def shape(text):
    # Reshape and then reverse for left-to-right drawing
    return get_display(reshaper.reshape(text))

img = Image.new('RGB', (width, height), color=bg_color)
draw = ImageDraw.Draw(img)

# 1. Header "الان تقریبا"
h_text = shape("الان تقریبا")
hb = draw.textbbox((0, 0), h_text, font=font_header)
draw.text((width - (hb[2]-hb[0]) - 5, -5), h_text, font=font_header, fill=text_color)

# 2. "ساعت"
saat_text = shape("ساعت")
sb = draw.textbbox((0, 0), saat_text, font=font_saat)
saat_w, saat_h = sb[2]-sb[0], sb[3]-sb[1]
saat_x = width - saat_w - 5
saat_y = 20
draw.text((saat_x, saat_y), saat_text, font=font_saat, fill=text_color)

# 3. "نه" (hour)
hour_text = shape("نه")
hob = draw.textbbox((0, 0), hour_text, font=font_hour)
hour_w, hour_h = hob[2]-hob[0], hob[3]-hob[1]
hour_x = width - hour_w - 5
hour_y = saat_y + 40
draw.text((hour_x, hour_y), hour_text, font=font_hour, fill=text_color)

# 4. "نیم" (modifier)
mod_text = shape("نیم")
mb = draw.textbbox((0, 0), mod_text, font=font_mod)
mod_w, mod_h = mb[2]-mb[0], mb[3]-mb[1]
mod_x = hour_x - mod_w - 2
mod_y = saat_y + 35
draw.text((mod_x, mod_y), mod_text, font=font_mod, fill=text_color)

# 5. "و" (connector)
conn_text = shape("و")
cb = draw.textbbox((0, 0), conn_text, font=font_conn)
conn_w, conn_h = cb[2]-cb[0], cb[3]-cb[1]
conn_x = mod_x + 10
conn_y = mod_y - 8
draw.text((conn_x, conn_y), conn_text, font=font_conn, fill=text_color)

# Convert to 1-bit WITH NO DITHERING. This fixes the "low quality" noise/fuzziness!
img = img.convert('1', dither=Image.NONE)
img.save("test_layout_crisp.png")
print("Saved test_layout_crisp.png")
