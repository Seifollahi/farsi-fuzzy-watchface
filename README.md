# Farsi Fuzzy Watchface

A stunning, native Farsi fuzzy time watchface for Pebble smartwatches, written from the ground up for maximum visual impact and cultural authenticity.

## Features

- **Calligraphic Typography:** Custom-built using the massive, interlocking `Lalezar` and `Vazirmatn-Black` font engine for a premium, artistic look on your wrist.
- **Dynamic Fuzzy Time:** Reads out the time exactly how Farsi speakers naturally say it (e.g., "ساعت ده و نیم", "یک ربع به شش").
- **Multiple Accuracies:** Choose between 15-minute intervals, 30-minute intervals, exact hours, or even loose daily periods ("صبحه").
- **Anti-Aliasing:** Harnesses Pebble's hardware and a custom grayscale layout generator to create silky smooth curves—a rarity on Pebble's 1-bit or 2-bit color space!
- **Theme Toggle:** Instantly switch between **Dark Mode** (White on Black) and **Light Mode** (Black on White) directly from the Pebble app configuration page! No memory overhead.

## Screenshots

<div style="display: flex; gap: 10px;">
  <img src="screenshots/appstore/screenshot_1_dark.png" width="144" />
  <img src="screenshots/appstore/screenshot_2_light.png" width="144" />
  <img src="screenshots/appstore/screenshot_3_dark.png" width="144" />
  <img src="screenshots/appstore/screenshot_4_light.png" width="144" />
</div>

## Changelog

### v2.8.0
- **Feature:** Full Light/Dark theme toggle in Pebble Config app.
- **Enhancement:** Watchface utilizes native Pebble palette manipulation for instant theme switching with 0% memory overhead.
- **Bugfix:** Resolved `TUPLE_INT32` memory alignment issues from PebbleKit JS payload.
- **Bugfix:** Pebble configuration page now securely caches settings via `localStorage`.

### v2.6.0
- **Redesign:** Transitioned to heavy, calligraphic typography (Vazirmatn-Black).
- **Enhancement:** Introduced a custom Python cluster-layout algorithm to securely overlap and interlock Farsi words, creating a beautiful piece of art.
- **Enhancement:** Enabled anti-aliasing via grayscale output to significantly improve jagged edges.

### v1.0.0
- Initial release using standard layout and fonts.

## Installation

Download the latest `app.pbw` from the [Releases](https://github.com/MakeAwesomeHappen/farsi_fuzzy_watchface/releases) page and sideload it to your phone using the Rebble App.

## Building from source

1. Run the Python generation script to create the 57 unique time states:
   ```bash
   python3 generate_bitmaps.py
   ```
2. Build the PBW using the Pebble SDK:
   ```bash
   docker run --rm -v "$(pwd):/app" -w /app rebble/pebble-sdk pebble build
   ```
