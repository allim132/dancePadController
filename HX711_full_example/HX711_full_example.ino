#include "HX711.h"

// AI improvements

// Pin definitions
const int HX711_dout1 = 3;
const int HX711_sck1  = 2;

const int HX711_dout2 = 5;
const int HX711_sck2  = 4;

const int HX711_dout3 = 7;
const int HX711_sck3  = 6;

const int HX711_dout4 = 9;
const int HX711_sck4  = 8;

// Calibration values: you should calibrate each sensor separately
const float SCALE_1 = 2280.0f;
const float SCALE_2 = 2280.0f;
const float SCALE_3 = 2280.0f;
const float SCALE_4 = 2280.0f;

// Smoothing factor: higher = smoother, but more latency
const float ALPHA = 0.35f;

HX711 scale1;
HX711 scale2;
HX711 scale3;
HX711 scale4;

float filtered1 = 0.0f;
float filtered2 = 0.0f;
float filtered3 = 0.0f;
float filtered4 = 0.0f;

float readScaleFiltered(HX711 &scale, float &filteredValue) {
  // Avoid blocking forever
  if (!scale.wait_ready_timeout(5)) {
    return filteredValue;  // keep previous value if no new sample yet
  }

  float raw = scale.get_units(1);  // 1 sample to minimize delay
  raw = abs(raw);

  // Exponential moving average
  filteredValue = ALPHA * raw + (1.0f - ALPHA) * filteredValue;
  return filteredValue;
}

void setup() {
  Serial.begin(115200);

  scale1.begin(HX711_dout1, HX711_sck1);
  scale2.begin(HX711_dout2, HX711_sck2);
  scale3.begin(HX711_dout3, HX711_sck3);
  scale4.begin(HX711_dout4, HX711_sck4);

  scale1.set_scale(SCALE_1);
  scale2.set_scale(SCALE_2);
  scale3.set_scale(SCALE_3);
  scale4.set_scale(SCALE_4);

  scale1.tare();
  scale2.tare();
  scale3.tare();
  scale4.tare();
}

void loop() {
  float w = readScaleFiltered(scale1, filtered1);
  float a = readScaleFiltered(scale2, filtered2);
  float s = readScaleFiltered(scale3, filtered3);
  float d = readScaleFiltered(scale4, filtered4);

  // Compact CSV output: W,A,S,D
  Serial.print(w, 2);
  Serial.print(",");
  Serial.print(a, 2);
  Serial.print(",");
  Serial.print(s, 2);
  Serial.print(",");
  Serial.println(d, 2);

  // Small delay to keep serial stable without adding much latency
  delay(1);
}