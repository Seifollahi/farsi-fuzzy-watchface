#include <pebble.h>
#include "farsi_bitmaps.h"

#define PERSIST_KEY_ACCURACY 1
#define PERSIST_KEY_THEME_COLOR 2
#define DEFAULT_ACCURACY ACCURACY_QUARTER
#define DEFAULT_THEME 0

static Window *s_main_window;
static BitmapLayer *s_main_layer;
static GBitmap *s_current_bitmap = NULL;
static int s_accuracy;
static int s_theme_color;

static int get_period(int hour) {
  if (hour >= 5 && hour <= 11) return 0;
  else if (hour >= 12 && hour <= 13) return 1;
  else if (hour >= 14 && hour <= 16) return 2;
  else if (hour >= 17 && hour <= 19) return 3;
  else return 4;
}

static void invert_bitmap(GBitmap *bmp) {
  uint8_t *data = gbitmap_get_data(bmp);
  uint16_t row_size_bytes = gbitmap_get_bytes_per_row(bmp);
  GRect bounds = gbitmap_get_bounds(bmp);
  GBitmapFormat format = gbitmap_get_format(bmp);
  
  if (format == GBitmapFormat1Bit) {
    for (int y = 0; y < bounds.size.h; y++) {
      for (int x = 0; x < row_size_bytes; x++) {
        data[y * row_size_bytes + x] = ~data[y * row_size_bytes + x];
      }
    }
  } else if (format == GBitmapFormat8Bit) {
    for (int y = 0; y < bounds.size.h; y++) {
      for (int x = 0; x < row_size_bytes; x++) {
        data[y * row_size_bytes + x] ^= 0b00111111; // Invert RGB bits, keep Alpha
      }
    }
  } else {
    // Palette formats: 1BitPalette, 2BitPalette, 4BitPalette, 8BitPalette
    GColor *palette = gbitmap_get_palette(bmp);
    if (palette) {
      int num_colors = 0;
      if (format == GBitmapFormat1BitPalette) num_colors = 2;
      else if (format == GBitmapFormat2BitPalette) num_colors = 4;
      else if (format == GBitmapFormat4BitPalette) num_colors = 16;
      else num_colors = 256; // Fallback for 8BitPalette if it exists
      
      for (int i = 0; i < num_colors; i++) {
        palette[i].argb ^= 0b00111111; // Invert RGB bits, keep Alpha
      }
    }
  }
}

static void update_time() {
  time_t temp = time(NULL);
  struct tm *tick_time = localtime(&temp);

  int hour = tick_time->tm_hour;
  int min = tick_time->tm_min;
  int hour_12 = hour % 12;

  uint32_t current_res_id = 0;

  switch (s_accuracy) {
    case ACCURACY_QUARTER: {
      int bucket = 0;
      if (min <= 7)       bucket = 0;
      else if (min <= 22) bucket = 1;
      else if (min <= 37) bucket = 2;
      else if (min <= 52) bucket = 3;
      else { bucket = 0; hour_12 = (hour_12 + 1) % 12; }
      current_res_id = FARSI_QUARTER[hour_12][bucket];
      break;
    }
    case ACCURACY_HALF: {
      int bucket = (min <= 15 || min >= 46) ? 0 : 1;
      if (min >= 46) hour_12 = (hour_12 + 1) % 12;
      current_res_id = FARSI_HALF[hour_12][bucket];
      break;
    }
    case ACCURACY_HOUR: {
      if (min >= 30) hour_12 = (hour_12 + 1) % 12;
      current_res_id = FARSI_HOUR[hour_12];
      break;
    }
    case ACCURACY_HALF_DAY: {
      current_res_id = FARSI_HALF_DAY[hour >= 12 ? 1 : 0];
      break;
    }
    case ACCURACY_DAY_NIGHT: {
      current_res_id = FARSI_DAY_NIGHT[(hour >= 6 && hour < 18) ? 0 : 1];
      break;
    }
    case ACCURACY_PERIOD: {
      current_res_id = FARSI_PERIOD[get_period(hour)];
      break;
    }
    default:
      current_res_id = FARSI_QUARTER[hour_12][0];
      break;
  }

  // Swap out bitmap
  if (s_current_bitmap) {
    gbitmap_destroy(s_current_bitmap);
  }
  
  s_current_bitmap = gbitmap_create_with_resource(current_res_id);
  
  if (s_theme_color == 1) {
    invert_bitmap(s_current_bitmap);
  }
  
  bitmap_layer_set_bitmap(s_main_layer, s_current_bitmap);
}

static void tick_handler(struct tm *tick_time, TimeUnits units_changed) {
  update_time();
}

static void inbox_received_callback(DictionaryIterator *iter, void *context) {
  Tuple *accuracy_tuple = dict_find(iter, MESSAGE_KEY_AccuracyLevel);
  if (accuracy_tuple) {
    s_accuracy = accuracy_tuple->value->int32;
    if (s_accuracy < 0 || s_accuracy > 5) s_accuracy = DEFAULT_ACCURACY;
    persist_write_int(PERSIST_KEY_ACCURACY, s_accuracy);
    update_time();
  }

  Tuple *theme_tuple = dict_find(iter, MESSAGE_KEY_ThemeColor);
  if (theme_tuple) {
    s_theme_color = theme_tuple->value->uint8;
    persist_write_int(PERSIST_KEY_THEME_COLOR, s_theme_color);
    update_time();
  }
}

static void main_window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_bounds(window_layer);

  window_set_background_color(window, GColorWhite); // Set white BG, so if bitmap is transparent, it's white. Actually, we should probably set it depending on theme, but bitmap covers whole screen so it doesn't matter.
  
  s_main_layer = bitmap_layer_create(bounds);
  bitmap_layer_set_compositing_mode(s_main_layer, GCompOpSet);
  layer_add_child(window_layer, bitmap_layer_get_layer(s_main_layer));
}

static void main_window_unload(Window *window) {
  bitmap_layer_destroy(s_main_layer);
  if (s_current_bitmap) {
    gbitmap_destroy(s_current_bitmap);
  }
}

static void init() {
  if (persist_exists(PERSIST_KEY_ACCURACY)) {
    s_accuracy = persist_read_int(PERSIST_KEY_ACCURACY);
  } else {
    s_accuracy = DEFAULT_ACCURACY;
  }

  if (persist_exists(PERSIST_KEY_THEME_COLOR)) {
    s_theme_color = persist_read_int(PERSIST_KEY_THEME_COLOR);
  } else {
    s_theme_color = DEFAULT_THEME;
  }

  s_main_window = window_create();
  window_set_window_handlers(s_main_window, (WindowHandlers) {
    .load = main_window_load,
    .unload = main_window_unload
  });
  window_stack_push(s_main_window, true);

  tick_timer_service_subscribe(MINUTE_UNIT, tick_handler);
  app_message_register_inbox_received(inbox_received_callback);
  app_message_open(64, 64);

  update_time();
}

static void deinit() {
  window_destroy(s_main_window);
}

int main(void) {
  init();
  app_event_loop();
  deinit();
}
