#include <Adafruit_NeoPixel.h>
#include <Servo.h>

#define PIN 7
#define NUMPIXELS 122
#define BRIGHTNESS 10

Servo propL;
Servo propR;
int L = 9;
int R = 10;

int ch1;
int ch2;
int ch3;
int LPWM;
int RPWM;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {

pinMode(3, INPUT);
pinMode(5, INPUT);
pinMode(6, INPUT);
propL.attach(L);
propR.attach(R);
Serial.begin(9600);

propL.writeMicroseconds(1500);
propR.writeMicroseconds(1500);
}

void loop() {
  ch1 = pulseIn(3, HIGH, 25000);
  ch2 = pulseIn(5, HIGH, 25000);
  ch3 = pulseIn(6, HIGH, 25000);

  RPWM = ch1+15;
  LPWM = ch3+30;

  if (LPWM > 1900)
    LPWM = 1900;
  //else if (1500 < LPWM < 1900) LPWM = 1500 - (LPWM - 1500);
  //else if (1100 < LPWM < 1500) LPWM = 1500 + (1500 - LPWM);
  else if (LPWM < 1100) LPWM = 1100;
  
  if (RPWM > 1900) RPWM = 1900;
  else if (RPWM < 1100) RPWM = 1100;

  Serial.print("Channel 1:");
  Serial.println(LPWM);

  Serial.print("Channel 3:");
  Serial.println(RPWM);

  if(RPWM >1600 or RPWM < 1400);
  propR.writeMicroseconds((LPWM));
  if(LPWM >1600 or LPWM < 1400);
  propL.writeMicroseconds(abs(RPWM-3000));

  delay(10);
}
