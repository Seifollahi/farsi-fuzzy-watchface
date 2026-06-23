from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("screenshots", exist_ok=True)
os.makedirs("serve/assets", exist_ok=True)

bg_color = (0, 0, 0)
text_color = (255, 255, 255)
width = 144
height = 168

font_path = "resources/fonts/Vazirmatn-Bold.ttf"
font_header = ImageFont.truetype(font_path, 24)
font_main = ImageFont.truetype(font_path, 38)

def rev(s): return s[::-1]

def create_screenshot(filename, header, main_lines):
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Header is at top, right aligned
    header_rev = rev(header)
    bbox = draw.textbbox((0, 0), header_rev, font=font_header)
    w = bbox[2] - bbox[0]
    # Draw header (Pillow draws LTR, so reversed Farsi strings will show correctly!)
    draw.text((width - w - 5, 5), header_rev, font=font_header, fill=text_color)
    
    # Calculate total height of main text
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
        
    # Start Y to vertically center the block below header
    start_y = 40 + (128 - total_h) // 2
    if start_y < 40: start_y = 40
    
    y = start_y
    for i, l in enumerate(main_rev_lines):
        x = width - line_widths[i] - 5
        draw.text((x, y), l, font=font_main, fill=text_color)
        y += line_heights[i] + 5 # 5px padding between lines
        
    img.save(filename)

# Generate screenshots
create_screenshot("screenshots/preview.png", "ﺍﻟﺎﻥ ﺗﻘﺮﯾﺒﺎ", ["ﺳﺎﻋﺖ", "ﺩﻭﺍﺯﺩﻩ", "ﻭ ﺭﺑﻊ ﺍ"])
create_screenshot("screenshots/hour.png", "ﺍﻟﺎﻥ ﺗﻘﺮﯾﺒﺎ", ["ﺳﺎﻋﺖ", "ﻫﺸﺖ ﺍ"])
create_screenshot("screenshots/period.png", "ﺍﻟﺎﻥ ﺗﻘﺮﯾﺒﺎ", ["ﺑﻌﺪﺍﺯﻇﻬﺮﻩ"])

# Create Icon (144x144 and 48x48)
icon = Image.new('RGB', (144, 144), color=bg_color)
draw = ImageDraw.Draw(icon)
bb = draw.textbbox((0, 0), rev("ﻓﺎﺯﯼ"), font=font_main)
icon_w = bb[2] - bb[0]
icon_h = bb[3] - bb[1]
draw.text(((144 - icon_w)//2, (144 - icon_h)//2), rev("ﻓﺎﺯﯼ"), font=font_main, fill=text_color)
icon.save("serve/assets/icon_144.png")
icon_small = icon.resize((48, 48), Image.Resampling.LANCZOS)
icon_small.save("serve/assets/icon_48.png")

print("Generated screenshots and icons!")
