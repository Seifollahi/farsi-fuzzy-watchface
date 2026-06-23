import json, re

hours_farsi = [
    "ﺩﻭﺍﺯﺩﻩ",  # 0
    "ﯾﮏ",      # 1
    "ﺩﻭ",      # 2
    "ﺳﻪ",      # 3
    "ﭼﻬﺎﺭ",    # 4
    "ﭘﻨﺞ",     # 5
    "ﺷﺶ",      # 6
    "ﻫﻔﺖ",     # 7
    "ﻫﺸﺖ",     # 8
    "ﻧﻪ",      # 9
    "ﺩﻩ",      # 10
    "ﯾﺎﺯﺩﻩ",   # 11
]
next_hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]

def rev_line(s): return s[::-1]
def make_multiline(lines): return '\\n'.join(rev_line(l) for l in lines)

lines = []
lines.append('#pragma once')
lines.append('#include <pebble.h>')
lines.append('// Accuracy modes')
lines.append('#define ACCURACY_QUARTER    0')
lines.append('#define ACCURACY_HALF       1')
lines.append('#define ACCURACY_HOUR       2')
lines.append('#define ACCURACY_HALF_DAY   3')
lines.append('#define ACCURACY_DAY_NIGHT  4')
lines.append('#define ACCURACY_PERIOD     5')
lines.append('')
lines.append(f'static const char* const FARSI_HEADER = "{rev_line("ﺍﻟﺎﻥ ﺗﻘﺮﯾﺒﺎ")}";')

lines.append('static const char* const FARSI_QUARTER[12][4] = {')
for i in range(12):
    h = hours_farsi[i]
    nh = hours_farsi[next_hours[i]]
    exact = make_multiline(["ﺳﺎﻋﺖ", f"{h} ﺍ"])
    quarter = make_multiline(["ﺳﺎﻋﺖ", f"{h}", "ﻭ ﺭﺑﻊ ﺍ"])
    half = make_multiline(["ﺳﺎﻋﺖ", f"{h}", "ﻭ ﻧﯿﻢ ﺍ"])
    to_next = make_multiline(["ﯾﻪ ﺭﺑﻊ", "ﻣﻮﻧﺪﻩ ﺑﻪ", f"{nh}"])
    lines.append(f'  {{ "{exact}", "{quarter}", "{half}", "{to_next}" }},')
lines.append('};')

lines.append('static const char* const FARSI_HALF[12][2] = {')
for i in range(12):
    h = hours_farsi[i]
    exact = make_multiline(["ﺳﺎﻋﺖ", f"{h} ﺍ"])
    half = make_multiline(["ﺳﺎﻋﺖ", f"{h}", "ﻭ ﻧﯿﻢ ﺍ"])
    lines.append(f'  {{ "{exact}", "{half}" }},')
lines.append('};')

lines.append('static const char* const FARSI_HOUR[12] = {')
for i in range(12):
    h = hours_farsi[i]
    exact = make_multiline(["ﺳﺎﻋﺖ", f"{h} ﺍ"])
    lines.append(f'  "{exact}",')
lines.append('};')

lines.append(f'static const char* const FARSI_HALF_DAY[2] = {{ "{rev_line("ﺻﺒﺤﻪ")}", "{rev_line("ﺷﺒﻪ")}" }};')
lines.append(f'static const char* const FARSI_DAY_NIGHT[2] = {{ "{rev_line("ﺭﻭﺯﻩ")}", "{rev_line("ﺷﺒﻪ")}" }};')
lines.append(f'static const char* const FARSI_PERIOD[5] = {{ "{rev_line("ﺻﺒﺤﻪ")}", "{rev_line("ﻇﻬﺮﻩ")}", "{rev_line("ﺑﻌﺪﺍﺯﻇﻬﺮﻩ")}", "{rev_line("ﻋﺼﺮﻩ")}", "{rev_line("ﺷﺒﻪ")}" }};')

with open('src/c/farsi_strings.h', 'w', encoding='utf-8') as f: f.write('\n'.join(lines))

with open("src/c/farsi_strings.h") as f:
    content = f.read()
chars = set()
for match in re.findall(r"\"([^\"]+)\"", content):
    for c in match:
        if c != "\\" and c != "n": chars.add(c)
codepoints = sorted(set(ord(c) for c in chars))
with open("farsi_chars.json", "w") as f: json.dump({"codepoints": codepoints}, f)

print(f"Generated farsi_strings.h and farsi_chars.json with {len(codepoints)} unique characters.")
