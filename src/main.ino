/***
 *       Filename:  noise_detector.ino
 *
 *    Description:  Project file.
 *
 *        Version:  0.0.1
 *        Created:  2016-07-10

 *       Revision:  none
 *
 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 *
 *        License:  GNU GPL2
 */

#define WINDOW_SIZE 20
#define NUMBER_OF_BUTTONS 7
#define READ_DELAY     2
#define WRITE_DELAY    10

/*  Running mean of signal. */
float running_mean_ = 0.0;

/*  List of buttons to get input from 
 *  PIN-13 is never a good idea as input/output pin
 */
int buttonList_[NUMBER_OF_BUTTONS] = { 12, 11, 10, 9, 8, 7, 6 };

/**
 * @brief Input from button is stored here.
 */
int input_[NUMBER_OF_BUTTONS] = {0, 0, 0, 0, 0, 0};

int num_of_buttons_pressed_ = 0;

// the setup routine runs once when you press reset:
void setup()
{
    // initialize serial communication at 9600 bits per second:
    Serial.begin(19200);

    // Set the button to be read-only. 
    for (size_t i = 0; i < NUMBER_OF_BUTTONS; i++) 
        pinMode( buttonList_[i], INPUT );

}

/**
 * @brief Print the read input onto serial port. Does nothing else. 
 * Only for debugging purpose.
 */
void printInput( )
{
    for (unsigned int i = 0; i < NUMBER_OF_BUTTONS; i++) 
    {
        Serial.print( input_[i] );
        Serial.print( ' ' );
    }
}

/**
 * @brief This function reads the input from buttons and does nothing else.
 * It will keep these values in global array input_
 */
unsigned long readInput( void )
{
    unsigned long sum = 0;
    for (unsigned int i = 0; i < NUMBER_OF_BUTTONS; i++) 
    {
        int val = digitalRead( buttonList_[i] );
        sum = sum + pow(4, i) * val;
        //Serial.println( val );
        input_[i] = val; 
        delay(READ_DELAY);
    }
    return sum;
}

int waitForKeypress( void )
{
    int val = -1;
    while(true)
    {
        for (size_t i = 0; i < NUMBER_OF_BUTTONS; i++) 
        {
            delay(READ_DELAY);
            val = digitalRead( buttonList_[i] );
            if( val == 1 )
                return i;
        }
    }
    return -1;
}

void pressButton( unsigned int buttonId )
{
    // Press button no buttonId 
    pinMode( buttonList_[ buttonId ], OUTPUT );
    digitalWrite( buttonList_[ buttonId ], HIGH );
    delay( WRITE_DELAY );
    pinMode( buttonList_[ buttonId ], INPUT );
}

/**
 * @brief Does the testing.
 */
void test( void )
{
    // Read from serial port the number of button.
    if( Serial.available() > 0 )
    {
        int buttonId = Serial.read();
        buttonId -= 48;
        if( buttonId < NUMBER_OF_BUTTONS )
        {
            Serial.print( " Pressed button " );
            Serial.print( buttonId );
            Serial.print( " " );
            Serial.println( num_of_buttons_pressed_ );
            num_of_buttons_pressed_ += 1;
            num_of_buttons_pressed_ = num_of_buttons_pressed_ % NUMBER_OF_BUTTONS;
            input_[ num_of_buttons_pressed_ ] = buttonId;
        }

        if( num_of_buttons_pressed_ == 0 )
        {
            Serial.println( "Time to match the sequence" );
        }

    }
}

// the loop routine runs over and over again forever:
void loop() 
{
    // read the input on analog pin 0:
    //readInput();
    // For debug purpose, print the values read.
    //printInput( );
    //setOutput();

    test( );
}
