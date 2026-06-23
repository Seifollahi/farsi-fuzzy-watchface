from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("screenshots/appstore", exist_ok=True)

bg_color = (0, 0, 0)
text_color = (255, 255, 255)

font_path = "resources/fonts/Vazirmatn-Bold.ttf"
try:
    font_main = ImageFont.truetype(font_path, 38)
    font_header = ImageFont.truetype(font_path, 24)
    font_banner_title = ImageFont.truetype(font_path, 64)
    font_banner_sub = ImageFont.truetype(font_path, 32)
except IOError:
    print("Error loading fonts.")
    exit(1)

def rev(s): return s[::-1]

# 1. 144x144 Logo and 48x48 Icon
def create_logos():
    icon = Image.new('RGB', (144, 144), color=bg_color)
    draw = ImageDraw.Draw(icon)
    # Draw "فازی" in the center
    text = rev("ﻓﺎﺯﯼ")
    bb = draw.textbbox((0, 0), text, font=font_main)
    w = bb[2] - bb[0]
    h = bb[3] - bb[1]
    draw.text(((144 - w)//2, (144 - h)//2 - 10), text, font=font_main, fill=text_color)
    
    icon.save("screenshots/appstore/appstore_logo.png")
    
    icon_small = icon.resize((48, 48), Image.Resampling.LANCZOS)
    icon_small.save("screenshots/appstore/appstore_icon_48.png")
    print("Generated Logos")

# 2. 720x320 Banner
def create_banner():
    img = Image.new('RGB', (720, 320), color=(15, 15, 15))
    draw = ImageDraw.Draw(img)
    
    # Paste logo
    logo = Image.open("screenshots/appstore/appstore_logo.png")
    img.paste(logo, (80, 88))
    
    # Text (LTR rendering of reversed strings)
    title = rev("ﺳﺎﻋﺖ ﻓﺎﺯﯼ") # Farsi Fuzzy Time
    sub1 = rev("ﺳﺒﮏ ﺯﻧﺪﮔﯽ‌ﺗﻮﻥ ﺭﻭ ﻋﻮﺽ ﮐﻨﯿﺪ") # Change your lifestyle
    sub2 = rev("ﺍﻭﻟﯿﻦ ﻭﺍﭺ‌ﻓﯿﺲ ﻓﺎﺭﺳﯽ ﭘﺒﻞ") # First Farsi Pebble watchface
    
    draw.text((280, 80), title, font=font_banner_title, fill=(255, 255, 255))
    draw.text((280, 170), sub1, font=font_banner_sub, fill=(200, 200, 200))
    draw.text((280, 220), sub2, font=font_banner_sub, fill=(150, 150, 150))
    
    img.save('screenshots/appstore/appstore_banner.png')
    print("Generated Banner")

# 3. Platform Screenshots
def create_screenshot(filename, width, height, header, main_lines):
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    header_rev = rev(header)
    bbox = draw.textbbox((0, 0), header_rev, font=font_header)
    w = bbox[2] - bbox[0]
    draw.text((width - w - int(width*0.05), int(height*0.05)), header_rev, font=font_header, fill=text_color)
    
    main_rev_lines = [rev(l) for l in main_lines]
    total_h = 0
    line_heights = []
    line_widths = []
    
    for l in main_rev_lines:
        bb = draw.textbbox((0, 0), l, font=font_main)
        lw = bb[2] - bb[0]
        lh = bb[3] - bb[1]
        line_widths.append(lw)
        line_heights.append(lh)
        total_h += lh
        
    start_y = int(height*0.25) + (int(height*0.75) - total_h) // 2
    if start_y < int(height*0.25): start_y = int(height*0.25)
    
    y = start_y
    for i, l in enumerate(main_rev_lines):
        x = width - line_widths[i] - int(width*0.05)
        draw.text((x, y), l, font=font_main, fill=text_color)
        y += line_heights[i] + 5
        
    img.save(filename)

def generate_all_screenshots():
    platforms = [
        ("aplite", 144, 168),
        ("basalt", 144, 168),
        ("diorite", 144, 168),
        ("chalk", 180, 180),
        ("emery", 200, 228)
    ]
    
    screens = [
        ("1", "ﺍﻟﺎﻥ ﺗﻘﺮﯾﺒﺎ", ["ﺳﺎﻋﺖ", "ﺩﻭﺍﺯﺩﻩ", "ﻭ ﺭﺑﻊ ﺍ"]),
        ("2", "ﺍﻟﺎﻥ ﺗﻘﺮﯾﺒﺎ", ["ﺳﺎﻋﺖ", "ﻫﺸﺖ ﺍ"]),
        ("3", "ﺍﻟﺎﻥ ﺗﻘﺮﯾﺒﺎ", ["ﺑﻌﺪﺍﺯﻇﻬﺮﻩ"])
    ]
    
    for plat, w, h in platforms:
        for idx, header, lines in screens:
            create_screenshot(f"screenshots/appstore/{plat}_{idx}.png", w, h, header, lines)
    print("Generated Platform Screenshots")

if __name__ == "__main__":
    create_logos()
    create_banner()
    generate_all_screenshots()
