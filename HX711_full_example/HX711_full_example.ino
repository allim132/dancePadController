#include "HX711.h"

// AI improvements

// Pin definitions
const int HX711_dout1 = 9; // 3
const int HX711_sck1  = 8; // 2
// W
const int HX711_dout2 = 3; // 3
const int HX711_sck2  = 2; // 2
// A
const int HX711_dout3 = 7;
const int HX711_sck3  = 6;
// S
const int HX711_dout4 = 5; // 5
const int HX711_sck4  = 4; // 4
// D

// Calibration values: you should calibrate each sensor separately
// const float SCALE_1 = 2280.0f;
// const float SCALE_2 = 2280.0f;
// const float SCALE_3 = 2280.0f;
// const float SCALE_4 = 2280.0f;

// Smoothing factor: higher = smoother, but more latency
const float ALPHA = 0.35f;

HX711 scale1;
HX711 scale2;
HX711 scale3;
HX711 scale4;


void setup() {
  Serial.begin(115200);
  // Initialize library with data output pin, clock input pin and gain factor.
  // Channel selection is made by passing the appropriate gain:
  // - With a gain factor of 64 or 128, channel A is selected
  // - With a gain factor of 32, channel B is selected
  // By omitting the gain factor parameter, the library
  // default "128" (Channel A) is used here.
  scale1.begin(HX711_dout1, HX711_sck1);
  scale1.set_scale(2280.f);                    
  scale1.tare();
  scale2.begin(HX711_dout2, HX711_sck2);
  scale2.set_scale(2280.f);                    
  scale2.tare();
  scale3.begin(HX711_dout3, HX711_sck3);
  scale3.set_scale(2280.f);                    
  scale3.tare();
  scale4.begin(HX711_dout4, HX711_sck4);
  scale4.set_scale(2280.f);                    
  scale4.tare();
}

void loop() {
  Serial.print("W: ");
  Serial.print(scale1.get_units());
  Serial.print(" S: ");
  Serial.print(scale2.get_units());
  Serial.print(" D: ");
  Serial.print(scale3.get_units());
  Serial.print(" A: ");
  Serial.println(scale4.get_units());
}