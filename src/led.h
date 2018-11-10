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
LPD8806 progressBarLed = LPD8806( 8, 34, 35 );
LPD8806 ca1LED = LPD8806( 21, 32, 33 );


LPD8806 axon0 = LPD8806( 31, 22, 23 );
LPD8806 axon1 = LPD8806( 31, 24, 25 );
LPD8806 axon2 = LPD8806( 31, 26, 27 );
LPD8806 axon3 = LPD8806( 31, 28, 29 );

LPD8806* axons[] = { &axon0, &axon1, &axon2, &axon3 };

int maxIndex( double* array, size_t len )
{
    float max = 0;
    size_t maxi = 0;
    for( size_t i = 0; i < len; i ++ )
    {
        if( array[i] > max )
        {
            max = array[i];
            maxi = i;
        }

    }
    return maxi;
}

void resetAllLEDs( )
{
    //  Show the progress bar.
    for (size_t i = 0; i < progressBarLed.numPixels( ); i++) 
    {
        uint32_t color = progressBarLed.Color( 0, 0, 0 );
        progressBarLed.setPixelColor( i, color );
        progressBarLed.show( );
    }

    for (size_t i = 0; i < ca1LED.numPixels( ); i++) 
    {
        uint32_t color = ca1LED.Color( 0, 0, 0 );
        ca1LED.setPixelColor( i, color );
        ca1LED.show( );
    }

}

// Chase one dot down the full strip.
void colorChase(LPD8806* strip, uint8_t wait )
{
    // Start by turning all pixels off:
    for(size_t i=0; i<strip->numPixels(); i++) strip->setPixelColor(i, 0);

    // Then display one pixel at a time:
    for(size_t i=0; i<strip->numPixels(); i++) 
    {
        strip->setPixelColor(i, strip->Color(0,0,127)); // Set new pixel 'on'
        strip->show();              // Refresh LED states
        strip->setPixelColor(i, 0); // Erase pixel, but don't refresh!
        delay(wait);
    }

    strip->show(); // Refresh to turn off last pixel
}

void lighupAxon( int buttonId )
{
    int axonId = buttonId / 2;
    colorChase( axons[ axonId ], 10 );
    // Serial.print( "Axon lighening up : " );
    // Serial.println( axonId );
}


// Show progress bar.
void progressBar( double* match, size_t len )
{
    size_t maxI = maxIndex( match, len );
    float maxVal = match[ maxI ];
    // Serial.println( "Display progress bar" );
    size_t c = (127 * maxVal) / len;

    //  Show the progress bar.
    for (size_t i = 0; i < progressBarLed.numPixels( ); i++) 
    {
        uint32_t color = progressBarLed.Color( 0, 0, 0 );
        if( i <  (progressBarLed.numPixels() * maxVal / len) )
            color = progressBarLed.Color( c, c, c );

        progressBarLed.setPixelColor( i, color );
        progressBarLed.show( );
    }

    // Associate in ca1. Winner takes all.
    int ca1Array[ ] = { 0, 3, 7, 14, 17, 21 };

    for (size_t i = 0; i < ca1LED.numPixels( ); i++) 
    {
        uint32_t color = ca1LED.Color( 0, 0, 0 );
        if( (size_t)ca1Array[maxI] == i ) 
            color = ca1LED.Color( c, c, c );
        ca1LED.setPixelColor( i, color );
        ca1LED.show( );
    }
}

#endif   /* ----- #ifndef led_INC  ----- */
