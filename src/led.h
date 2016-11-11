/*
 * =====================================================================================
 *
 *       Filename:  led.h
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  11/02/2016 11:05:06 AM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 * =====================================================================================
 */

#ifndef  led_INC
#define  led_INC

#include "LPD8806/LPD8806.h"

#define NUMBER_OF_STRIPS 1

int n_leds[] = { 8, 8, 8, 8 };
int clock_pins_[] =  { 22, 24, 26, 28, 30 };
int data_pins_[] = { 23, 25, 27, 29, 31 };


LPD8806 strip = LPD8806( 9, 22, 23 );
LPD8806 progressBarLed = LPD8806( 16, 24, 25 );

// Chase one dot down the full strip.
void colorChase(LPD8806* strip, uint32_t c, uint8_t wait, unsigned strip_index = 0) 
{
    int i;

    // Start by turning all pixels off:
    for(i=0; i<strip->numPixels(); i++) strip->setPixelColor(i, 0);

    // Then display one pixel at a time:
    for(i=0; i<strip->numPixels(); i++) {
        strip->setPixelColor(i, c); // Set new pixel 'on'
        strip->show();              // Refresh LED states
        strip->setPixelColor(i, 0); // Erase pixel, but don't refresh!
        delay(wait);
    }

    strip->show(); // Refresh to turn off last pixel
}


void progressBar( double* match, int len )
{
    Serial.println( "Display progress bar" );
    colorChase(&progressBarLed, progressBarLed.Color(127, 127, 127), 10); // White
}

#endif   /* ----- #ifndef led_INC  ----- */
