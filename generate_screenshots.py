import os
from PIL import Image, ImageOps

source_dir = "resources/images/"
out_dir = "screenshots/appstore/"

os.makedirs(out_dir, exist_ok=True)

# Select 5 cool phrases to showcase
# exact_10 = 10:00 (ساعت ده)
# half_4 = 4:30 (ساعت چهار و نیم)
# quarter_2 = 2:15 (ساعت دو و ربع)
# tonext_8 = 8:45 (یک ربع به نه)
# halfday_0 = 12h (صبحه)

selections = [
    ("img_exact_10.png", "screenshot_1_dark.png", False),
    ("img_half_4.png", "screenshot_2_light.png", True),
    ("img_quarter_2.png", "screenshot_3_dark.png", False),
    ("img_tonext_8.png", "screenshot_4_light.png", True),
    ("img_exact_1.png", "screenshot_5_dark.png", False),
]

for src, dest, light_theme in selections:
    img_path = os.path.join(source_dir, src)
    if not os.path.exists(img_path):
        print(f"Missing {src}")
        continue
        
    img = Image.open(img_path).convert("L")
    
    if light_theme:
        img = ImageOps.invert(img)
        
    img.save(os.path.join(out_dir, dest))
    print(f"Generated {dest}")

    # The user specifically requested 200x228 white theme pictures
    if light_theme:
        # Create a new 200x228 white canvas
        padded_img = Image.new("L", (200, 228), color=255)
        # Paste the 144x168 image centered on the 200x228 canvas
        # x_offset = (200 - 144) // 2 = 28
        # y_offset = (228 - 168) // 2 = 30
        padded_img.paste(img, (28, 30))
        padded_dest = dest.replace(".png", "_200x228.png")
        padded_img.save(os.path.join(out_dir, padded_dest))
        print(f"Generated {padded_dest}")

print("Done generating App Store screenshots.")
