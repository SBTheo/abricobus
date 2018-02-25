#include <Adafruit_GFX.h>   // Core graphics library
#include <RGBmatrixPanel.h> // Hardware-specific library

// Similar to F(), but for PROGMEM string pointers rather than literals
#define F2(progmem_ptr) (const __FlashStringHelper *)progmem_ptr

#define CLK 8  // MUST be on PORTB! (Use pin 11 on Mega)
#define LAT A3
#define OE  9
#define A   A0
#define B   A1
#define C   A2
// Last parameter = 'true' enables double-buffering, for flicker-free,
// buttery smooth animation.  Note that NOTHING WILL SHOW ON THE DISPLAY
// until the first call to swapBuffers().  This is normal.
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, true);
// Double-buffered mode consumes nearly all the RAM available on the
// Arduino Uno -- only a handful of free bytes remain.  Even the
// following string needs to go in PROGMEM:

const char str[] PROGMEM = "Le bus arrive dans";
int    textX   = matrix.width(),
       textMin = sizeof(str) * -12,
       hue     = 0;
int8_t ball[3][4] = {
  {  3,  0,  1,  1 }, // Initial X,Y pos & velocity for 3 bouncy balls
  { 17, 15,  1, -1 },
  { 27,  4, -1,  1 }
};
static const uint16_t PROGMEM ballcolor[3] = {
  0x0080, // Green=1
  0x0002, // Blue=1
  0x1000  // Red=1
};

/* Constante pour la photo résistance
*/
int analogPin= A4;
int raw= 0;
int Vin= 5;
float Vout= 0;
float R1= 1000;
float R2= 0;
float buffer= 0;

void setup() {
  matrix.begin();
  matrix.setTextWrap(false); // Allow text to run off right edge
  matrix.setTextSize(2);

  Serial.begin(9600);
}

void loop() {
  byte i;

  // Clear background
  matrix.fillScreen(0);

  // Draw big scrolly text on top
  matrix.setTextColor(matrix.ColorHSV(hue, 255, 255, true));
  matrix.setCursor(textX, 1);
  matrix.print(F2(str));

  // Move text left (w/wrap), increase hue
  if((textX--) < textMin)
  { 
    matrix.fillScreen(0);
    matrix.setCursor(0, 1);   // start at one pixel left, with one pixel of spacing
    int donneesALire = Serial.available(); //lecture du nombre de caractères disponibles dans le buffer
    if(donneesALire > 0) //si le buffer n'est pas vide
    {
      //Il y a des données, on les lit et on fait du traitement
      char li = Serial.read(); 
      while(li != '@')
      {
        matrix.print(li);
        li = Serial.read();
      }
      /*matrix.print(li);
      matrix.print('m');*/
      matrix.swapBuffers(false);
      delay(5000);
    }
    textX = matrix.width();
  }
//  hue += 7;
//  if(hue >= 1536) hue -= 1536;

  // Update display
  matrix.swapBuffers(false);

  raw= analogRead(analogPin);
  if(raw) 
  {
          buffer= raw * Vin;
          Vout= (buffer)/1024.0;
          buffer= (Vin/Vout) -1; 
          R2= R1 * buffer;
          Serial.println(R2);
          //delay(1000);
  }
}
