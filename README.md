# Farsi Fuzzy Time (ساعت فازی فارسی)

![Screenshot](screenshots/preview.png)

Welcome to the **first-ever Farsi watchface** for the Pebble community! This isn't just an artistic, minimalist design—it's a lifestyle change. Instead of stressing over every minute and second, Farsi Fuzzy Time gives you the time the way humans actually talk: "It's almost noon" or "It's a quarter to twelve."

## Features
- **6 Configurable Accuracy Levels**: Choose how connected to the clock you want to be:
  1. **Quarter Hour (ربع ساعت)**: e.g. "ساعت دوازده و ربع ا"
  2. **Half Hour (نیم ساعت)**: e.g. "ساعت دوازده و نیم ا"
  3. **Hour (ساعت)**: e.g. "ساعت دوازده ا"
  4. **Half Day (نیم‌روز)**: AM / PM (صبحه / شبه)
  5. **Day / Night (روز و شب)**: Daytime vs Nighttime (روزه / شبه)
  6. **5-Periods (بخش‌های روز)**: Morning, Noon, Afternoon, Evening, Night
- **Beautiful Typography**: Uses the Vazirmatn font for clean, modern Arabic script rendering.
- **Companion App Settings**: Easily switch between accuracy modes right from the Pebble mobile app.

## The Technical Challenge
Pebble OS does **not** natively support Right-To-Left (RTL) text or Arabic script context-dependent shaping. Rendering Farsi text natively results in disconnected, backward letters.

To solve this, this watchface:
1. Uses a Python script to **pre-shape** and **fully reverse** every single Farsi string line by line.
2. Manually splits strings into appropriately sized lines to avoid Pebble's Left-To-Right word wrap algorithm (which would otherwise scramble the word order of reversed text).
3. Compiles a custom subset of the Vazirmatn font including only the exact codepoints needed to save precious RAM.

## Building from Source

1. Install the [Rebble Pebble SDK](https://help.rebble.io/sdk/).
2. Clone this repository.
3. If you edit the strings in the Python script, regenerate the headers and character lists:
   ```bash
   python3 generate_strings.py
   ```
4. Build the watchface:
   ```bash
   pebble build
   ```
5. Install on your watch or emulator:
   ```bash
   pebble install --emulator basalt
   ```

## License
MIT License. Feel free to fork and create your own fuzzy language variations!
