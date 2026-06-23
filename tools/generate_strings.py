import arabic_reshaper
from bidi.algorithm import get_display

words = {
    "STR_SAAT": "ساعت",
    "STR_YE": "یه",
    "STR_YEK": "یک",
    "STR_DO": "دو",
    "STR_SE": "سه",
    "STR_CHAHAR": "چهار",
    "STR_PANJ": "پنج",
    "STR_SHISH": "شش",
    "STR_HAFT": "هفت",
    "STR_HASHT": "هشت",
    "STR_NOH": "نه",
    "STR_DAH": "ده",
    "STR_YAZDAH": "یازده",
    "STR_DAVAZDAH": "دوازده",
    
    "STR_NIM": "نیم",
    "STR_ROB": "ربع",
    
    "STR_VA": "و",
    "STR_A": "ا", # for "است" or casual "ا"
    "STR_MONDE_BE": "مونده به",
    
    # Pre-baked sentences based on user preference
    # 1. Exact hour: "ساعت دو ا"
    # 2. Half past: "ساعت دو و نیم ا"
    # 3. Quarter to: "یه ربع مونده به سه"
}

# The user wants sentences that fit on the screen.
# To make formatting easier, we can pre-shape the ENTIRE sentence for each minute bucket!
# There are 12 hours * 4 minute buckets (exact, quarter past, half past, quarter to) = 48 strings.
# This is tiny in C (less than 2KB).
# Let's generate a C header with an array of strings.

hours = [
    "دوازده", "یک", "دو", "سه", "چهار", "پنج", "شش", 
    "هفت", "هشت", "نه", "ده", "یازده"
]

# For "Quarter to", we need the NEXT hour.
def get_next_hour(h):
    return hours[(h + 1) % 12]

c_code = """#pragma once
// Auto-generated Farsi shaped strings for LTR display

static const char* const FARSI_TIME_STRINGS[12][4] = {
"""

for h in range(12):
    current_hour_str = hours[h]
    next_hour_str = get_next_hour(h)
    
    # 0 = Exact hour
    s_exact = f"ساعت {current_hour_str} ا"
    
    # 1 = Quarter past
    s_q_past = f"ساعت {current_hour_str} و ربع ا"
    
    # 2 = Half past
    s_half = f"ساعت {current_hour_str} و نیم ا"
    
    # 3 = Quarter to
    s_q_to = f"یه ربع مونده به {next_hour_str}"
    
    phrases = [s_exact, s_q_past, s_half, s_q_to]
    
    c_code += "  {\n"
    for p in phrases:
        reshaped_text = arabic_reshaper.reshape(p)
        bidi_text = get_display(reshaped_text)
        # Escape for C
        c_code += f'    "{bidi_text}",\n'
    c_code += "  },\n"

c_code += "};\n"

with open("src/farsi_strings.h", "w", encoding="utf-8") as f:
    f.write(c_code)

print("Generated src/farsi_strings.h")
