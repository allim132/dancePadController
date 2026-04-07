/**
 *
 * HX711 library for Arduino - example file
 * https://github.com/bogde/HX711
 *
 * MIT License
 * (c) 2018 Bogdan Necula
 *
**/
#include "HX711.h"


// HX711 circuit wiring
const int HX711_dout1 = 3;
const int HX711_sck1 = 2;

const int HX711_dout2 = 5; // Second Load Cell Data Pin
const int HX711_sck2 = 4; // Second Load Cell Clock Pin

const int HX711_dout3 = 7; // Third Load Cell Data Pin
const int HX711_sck3 = 6; // Third Load Cell Clock Pin

const int HX711_dout4 = 9; // Fourth Load Cell Data Pin
const int HX711_sck4 = 8; // Fourth Load Cell Clock Pin

const int threshold = 10; //Loadcell Threshold
HX711 scale1;
HX711 scale2;
HX711 scale3;
HX711 scale4;


void setup() {
  Serial.begin(9600);
  // Initialize library with data output pin, clock input pin and gain factor.
  // Channel selection is made by passing the appropriate gain:
  // - With a gain factor of 64 or 128, channel A is selected
  // - With a gain factor of 32, channel B is selected
  // By omitting the gain factor parameter, the library
  // default "128" (Channel A) is used here.
  scale1.begin(HX711_dout1, HX711_sck1);
  scale1.set_scale(2280.f);                    
  scale1.tare();
  // scale2.begin(HX711_dout2, HX711_sck2);
  // scale2.set_scale(2280.f);                    
  // scale2.tare();
  // scale3.begin(HX711_dout3, HX711_sck3);
  // scale3.set_scale(2280.f);                    
  // scale3.tare();
  // scale4.begin(HX711_dout4, HX711_sck4);
  // scale4.set_scale(2280.f);                    
  // scale4.tare();
}

void loop() {
  Serial.print("W: ");
  Serial.println(scale1.get_units());
  // Serial.print(" A: ");
  // Serial.print(scale2.get_units());
  // Serial.print(" S: ");
  // Serial.print(scale3.get_units());
  // Serial.print(" D: ");
  // Serial.println(scale4.get_units());
}


