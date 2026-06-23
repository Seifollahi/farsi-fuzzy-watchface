#include <pebble.h>
#include "farsi_strings.h"

#define PERSIST_KEY_ACCURACY 1
#define DEFAULT_ACCURACY ACCURACY_QUARTER

static Window *s_main_window;
static TextLayer *s_header_layer;
static TextLayer *s_main_layer;
static GFont s_header_font;
static GFont s_main_font;
static int s_accuracy;

// Get time-of-day period index (0-4) for 5-period mode
static int get_period(int hour) {
  if (hour >= 5 && hour <= 11) return 0;       // صبح morning
  else if (hour >= 12 && hour <= 13) return 1;  // ظهر noon
  else if (hour >= 14 && hour <= 16) return 2;  // بعدازظهر afternoon
  else if (hour >= 17 && hour <= 19) return 3;  // عصر evening
  else return 4;                                 // شب night
}

static void update_time() {
  time_t temp = time(NULL);
  struct tm *tick_time = localtime(&temp);

  int hour = tick_time->tm_hour;
  int min = tick_time->tm_min;
  int hour_12 = hour % 12;

  const char *main_text = "";

  switch (s_accuracy) {
    case ACCURACY_QUARTER: {
      int bucket = 0;
      if (min <= 7)       bucket = 0;
      else if (min <= 22) bucket = 1;
      else if (min <= 37) bucket = 2;
      else if (min <= 52) bucket = 3;
      else { bucket = 0; hour_12 = (hour_12 + 1) % 12; }
      main_text = FARSI_QUARTER[hour_12][bucket];
      break;
    }
    case ACCURACY_HALF: {
      int bucket = (min <= 15 || min >= 46) ? 0 : 1;
      if (min >= 46) hour_12 = (hour_12 + 1) % 12;
      main_text = FARSI_HALF[hour_12][bucket];
      break;
    }
    case ACCURACY_HOUR: {
      if (min >= 30) hour_12 = (hour_12 + 1) % 12;
      main_text = FARSI_HOUR[hour_12];
      break;
    }
    case ACCURACY_HALF_DAY: {
      main_text = FARSI_HALF_DAY[hour >= 12 ? 1 : 0];
      break;
    }
    case ACCURACY_DAY_NIGHT: {
      main_text = FARSI_DAY_NIGHT[(hour >= 6 && hour < 18) ? 0 : 1];
      break;
    }
    case ACCURACY_PERIOD: {
      main_text = FARSI_PERIOD[get_period(hour)];
      break;
    }
    default:
      main_text = FARSI_QUARTER[hour_12][0];
      break;
  }

  // Set header
  text_layer_set_text(s_header_layer, FARSI_HEADER);
  
  // Set main text
  text_layer_set_text(s_main_layer, main_text);

  // Vertically center main text below header
  Layer *window_layer = window_get_root_layer(s_main_window);
  GRect bounds = layer_get_bounds(window_layer);
  
  // Header takes top ~40px
  int header_h = 45;
  int main_area_h = bounds.size.h - header_h;
  
  GSize text_size = graphics_text_layout_get_content_size(
      main_text, s_main_font,
      GRect(0, 0, bounds.size.w, main_area_h),
      GTextOverflowModeWordWrap, GTextAlignmentRight);
  
  int y_offset = header_h + (main_area_h - text_size.h) / 2;
  if (y_offset < header_h) y_offset = header_h;
  
  layer_set_frame(text_layer_get_layer(s_main_layer),
      GRect(0, y_offset, bounds.size.w, bounds.size.h - y_offset));
}

static void tick_handler(struct tm *tick_time, TimeUnits units_changed) {
  update_time();
}

// AppMessage: receive accuracy setting from companion app
static void inbox_received_callback(DictionaryIterator *iter, void *context) {
  Tuple *accuracy_tuple = dict_find(iter, MESSAGE_KEY_AccuracyLevel);
  if (accuracy_tuple) {
    s_accuracy = accuracy_tuple->value->int32;
    if (s_accuracy < 0 || s_accuracy > 5) s_accuracy = DEFAULT_ACCURACY;
    persist_write_int(PERSIST_KEY_ACCURACY, s_accuracy);
    update_time();
  }
}

static void main_window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_bounds(window_layer);

  window_set_background_color(window, GColorBlack);

  // Load fonts
  s_header_font = fonts_load_custom_font(
      resource_get_handle(RESOURCE_ID_FONT_VAZIR_24));
  s_main_font = fonts_load_custom_font(
      resource_get_handle(RESOURCE_ID_FONT_VAZIR_BOLD_38));

  // Header layer: "الان تقریبا" — top right
  s_header_layer = text_layer_create(
      GRect(0, 5, bounds.size.w - 5, 35));
  text_layer_set_background_color(s_header_layer, GColorClear);
  text_layer_set_text_color(s_header_layer, GColorWhite);
  text_layer_set_text_alignment(s_header_layer, GTextAlignmentRight);
  text_layer_set_font(s_header_layer, s_header_font);
  layer_add_child(window_layer, text_layer_get_layer(s_header_layer));

  // Main layer: time text — large, right-aligned, below header
  s_main_layer = text_layer_create(
      GRect(0, 40, bounds.size.w, bounds.size.h - 45));
  text_layer_set_background_color(s_main_layer, GColorClear);
  text_layer_set_text_color(s_main_layer, GColorWhite);
  text_layer_set_text_alignment(s_main_layer, GTextAlignmentRight);
  text_layer_set_overflow_mode(s_main_layer, GTextOverflowModeWordWrap);
  text_layer_set_font(s_main_layer, s_main_font);
  layer_add_child(window_layer, text_layer_get_layer(s_main_layer));
}

static void main_window_unload(Window *window) {
  text_layer_destroy(s_header_layer);
  text_layer_destroy(s_main_layer);
  fonts_unload_custom_font(s_header_font);
  fonts_unload_custom_font(s_main_font);
}

static void init() {
  // Load persisted accuracy or default
  if (persist_exists(PERSIST_KEY_ACCURACY)) {
    s_accuracy = persist_read_int(PERSIST_KEY_ACCURACY);
  } else {
    s_accuracy = DEFAULT_ACCURACY;
  }

  s_main_window = window_create();
  window_set_window_handlers(s_main_window, (WindowHandlers) {
    .load = main_window_load,
    .unload = main_window_unload
  });
  window_stack_push(s_main_window, true);

  // Register tick handler
  tick_timer_service_subscribe(MINUTE_UNIT, tick_handler);

  // Register AppMessage
  app_message_register_inbox_received(inbox_received_callback);
  app_message_open(64, 64);

  // Show time immediately
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
