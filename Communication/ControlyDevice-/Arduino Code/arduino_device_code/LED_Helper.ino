// Some universal function for controlling WS28x Leds
void setRGBColor(CRGB _leds[], int pos, int color[3]) {
  _leds[pos].setRGB(color[0], color[1], color[2]);
}

void turnOn(int color[3], CRGB _leds[]) {
  fill_solid(leds, NUM_LEDS, CRGB(color[0],color[1],color[2]));
  FastLED.show();
}

void turnOff(bool rest, CRGB _leds[]) {
  if (rest) {
    turnOn(restColors, _leds);
  } else {
    int black[] = {0,0,0};
    turnOn(black, _leds);
  }
  FastLED.show();
}

void turnOnFromMiddle(int color[3], CRGB _leds[], int length) {
  int middle = length / 2;
  int n, m, t;
  // Even or odd
  if ((length % 2) == 0) {
    n = middle - 1;
    m = middle;
    t = middle - 1;
  } else {
    n = middle;
    m = middle;
    t = middle;
  }
  setRGBColor(_leds, n, color);
  setRGBColor(_leds, m, color);
  FastLED.show();

  int i = 0;
  while (i < t) {
    n--;
    m++;
    setRGBColor(_leds, n, color);
    setRGBColor(_leds, m, color);
    FastLED.show();

    i++;
    delay(10);
  }
}

void turnOffFromMiddle(bool rest, CRGB _leds[], int length) {
  if (rest) {
    turnOnFromMiddle(restColors, _leds, length);
  } else {
    int black[] = {0,0,0};
    turnOnFromMiddle(black, _leds, length);
  }
  FastLED.show();
}