#include <Adafruit_NeoPixel.h>

//
// Internet Ping Meter v1.0 - Eric Steed
//
// 01/03/17 - first version - EPS
//
// Set up variables
byte leds = 0;
uint8_t delayVal = 30;

// Set the PIN number that the NeoPixel is connected to
#define PIN   7

// How bright are the LED's (0-255).  These things put out
// a TON of light, so I added the ability to control the 
// brightness with a variable so it could be changed in one
// place to "turn it down".
#define INTENSITY 60

// Set color to Green to start
uint8_t  r = 0;
uint8_t  g = INTENSITY;
uint8_t  b = 0;

// Set the number of pixels on the NeoPixel
#define NUMPIXELS   12

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// Initialize everything and prepare to start
void setup()
{
  uint8_t i;

  // Set up the serial port for communication
  Serial.begin(9600);
  Serial.println("Started Serial Monitor");

  // This initializes the NeoPixel library.
  pixels.begin();

  // This sets all the pixels to "off"
  for (i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
    pixels.show();
  }

  // Cycle each pixel through the primary colors to make sure they work, then turn them all off
  // Red
  for (i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(INTENSITY, 0, 0));
    pixels.show();
    delay(delayVal);
  }

  // Green
  for (i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(0, INTENSITY, 0));
    pixels.show();
    delay(delayVal);
  }

  // Blue
  for (i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(0, 0, INTENSITY));
    pixels.show();
    delay(delayVal);
  }

  // White
  for (i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(INTENSITY, INTENSITY, INTENSITY));
    pixels.show();
    delay(delayVal);
  }

  // Turn off all LED's
  for (i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
    pixels.show();
  }
}

// Main loop
//
// When sending LED signals, send the color code first, then the number of LED's to
// turn on.  For example 6 Green LED's would be h6, 11 Red LED's would be db, all
// 12 LED's to Black would be ic
void loop()
{
  uint8_t i;
  if (Serial.available())
  {
    char ch = Serial.read();
    // Serial.print("ch = ");
    // Serial.println(ch);
    int led = ch - '0';

    // Serial.print("led = ");
    // Serial.println(led);

    // Define the color of the LED based on how many failures we have in a row
    // RED = 52(d)
    // ORANGE = 53(e)
    // YELLOW = 54(f)
    // YELLOW-GREEN = 55(g)
    // GREEN = 56(h)
    // BLACK = 57(i)

   
    switch (led) {
      // Set color to RED
      case 52: {
          r = INTENSITY;
          g = 0;
          b = 0;
        }
        break;

      // Set color to ORANGE
      case 53: {
          r = INTENSITY;
          g = (INTENSITY / 2);
          b = 0;
        }
        break;

      // Set color to YELLOW
      case 54: {
          r = INTENSITY;
          g = INTENSITY;
          b = 0;
        }
        break;

      // Set color to YELLOW-GREEN
      case 55: {
          r = (INTENSITY / 2);
          g = INTENSITY;
          b = 0;
        }
        break;

      // Set color to GREEN
      case 56: {
          r = 0;
          g = INTENSITY;
          b = 0;
        }
        break;

      // Set color to BLACK
      case 57: {
          r = 0;
          g = 0;
          b = 0;
        }
        break;

      // To save on code, if we receive a 0 through a 9, turn on that
      // number of LED's
      case 0 ... 9:
        for (i = 0; i < led; i++) {
          pixels.setPixelColor(i, pixels.Color(r, g, b));
          pixels.show();
        }
        break;

      // If we receive an "a", turn on 10 LED's
      case 49:
        for (i = 0; i < 10; i++) {
          pixels.setPixelColor(i, pixels.Color(r, g, b));
          pixels.show();
        }
        break;

      // If we receive a "b", turn on 11 LED's
      case 50:

        for (i = 0; i < 11; i++) {
          pixels.setPixelColor(i, pixels.Color(r, g, b));
          pixels.show();
        }
        break;

      // If we receive a "c", turn on 12 LED's
      case 51:

        for (i = 0; i < 12; i++) {
          pixels.setPixelColor(i, pixels.Color(r, g, b));
          pixels.show();
        }
        break;

      // For testing, insert a delay if we see a ,
      case -4:
        delay(delayVal * 10);
        break;

      default:
        // if nothing else matches, do the default
        // default is optional
        break;
    }
    // I had to add this bit of code to fix a problem where the Arduino buffer
    // apparently filled up after a very short time.  It would set the LED's on
    // but then pause for 2-3 seconds before it would receive the next command.
    // This tells the Arduino to flush out the buffer immediately.
    Serial.flush();
  }
}
