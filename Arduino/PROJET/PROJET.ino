// scrolltext demo for Adafruit RGBmatrixPanel library.
// Demonstrates double-buffered animation on our 16x32 RGB LED matrix:
// http://www.adafruit.com/products/420

// Written by Limor Fried/Ladyada & Phil Burgess/PaintYourDragon
// for Adafruit Industries.
// BSD license, all text above must be included in any redistribution.

#include <SPI.h> // librairie pour communiquer entre l'Arduino et le Raspberry

#include <Adafruit_GFX.h>   // Librairie pour le panneau 16x32
#include <RGBmatrixPanel.h> // Librairie spécifique

// Similar to F(), but for PROGMEM string pointers rather than literals
#define F2(progmem_ptr) (const __FlashStringHelper *)progmem_ptr

#define CLK 8  // branchement
#define LAT A3
#define OE  9
#define A   A0
#define B   A1
#define C   A2
// Last parameter = 'true' enables double-buffering, for flicker-free,
// buttery smooth animation.  Note that NOTHING WILL SHOW ON THE DISPLAY
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, true);
// Double-buffered mode consumes nearly all the RAM available on the
// Arduino Uno -- only a handful of free bytes remain.  Even the
// following string needs to go in PROGMEM:

// Déclaration de la chaine de caractère affichée
const char str[] PROGMEM = "Le bus arrive dans";
int    textX   = matrix.width(),
       textMin = sizeof(str) * -12,
       hue     = 0;
int8_t ball[3][4] = {
  {  3,  0,  1,  1 }, // 3 balles rebondisantes
  { 17, 15,  1, -1 },
  { 27,  4, -1,  1 }
};
static const uint16_t PROGMEM ballcolor[3] = {
  0x0080, // Vert=1
  0x0002, // Bleu=1
  0x1000  // Rouge=1
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

/* Initialisation des objets et variables
*/
void setup() {
  //pin de sorti pour tester la communication RPi <-> arduino
  pinMode(13, OUTPUT);
  //initialisation de l'objet matrix pour la matrice 16x32
  matrix.begin();
  matrix.setTextWrap(false); //Autoriser l'exécution du texte sur le bord droit
  matrix.setTextSize(2);

  //initialisation de la liaison série RPi <-> arduino
  Serial.begin(9600);
}

void loop() {
  byte i;

  // mettre le fond sans ecriture
  matrix.fillScreen(0);

  // definir la taille du texte, la couleur et la police
  matrix.setTextColor(matrix.ColorHSV(hue, 255, 255, true));
  matrix.setCursor(textX, 1);
  matrix.print(F2(str));
  delay(10);

  // bouger le texte vers la gauche (w/wrap), augmenter la teinte
  if((textX--) < textMin)
  { 
    matrix.fillScreen(0);
    matrix.setCursor(0, 1);   // commencer par écrire à partir de la gauche
    int donneesALire = Serial.available(); //lecture du nombre de caractères disponibles dans le buffer série RPi <-> arduino
    Serial.println(donneesALire);
    if(donneesALire > 0) //si le buffer n'est pas vide
    {
      //Il y a des données, on les lit tant qu'on a pas le caractère de fin '@' et on l'affiche sur la matrice
      char li = Serial.read();
      if(li == 'T')
      {
        li = Serial.read();
        while(li != '_')
        {
          matrix.print(li);
          li = Serial.read();
        }
        matrix.swapBuffers(false);
        delay(2000);
        matrix.fillScreen(0);
        matrix.setCursor(0, 1);
        li = Serial.read();
        while(li != '@')
        {
          matrix.print(li);
          li = Serial.read();
        }
        matrix.swapBuffers(false);
        delay(5000);
      }
      else
      {
        while(li != '@')
        {
          matrix.print(li);
          li = Serial.read();
        }
        matrix.swapBuffers(false);
        delay(5000);
      }
    }
    textX = matrix.width();
  }

  matrix.swapBuffers(false);

  //on lit la valeur de la tension de la photorésistance
  raw= analogRead(analogPin);
  if(raw) 
  {
    //on divise la valeur de la photoresistance par 1024.0
          buffer= raw * Vin;
          Vout= (buffer)/1024.0;
          buffer= (Vin/Vout) -1; 
          R2= R1 * buffer;
    //on envoit la valeur vers le RPi via le port série
          Serial.println(R2);
          //delay(200);
  }
}
