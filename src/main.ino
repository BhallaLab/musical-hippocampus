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

#include "pitches.h"
#include "led.h"

#define WINDOW_SIZE 20
#define NUMBER_OF_BUTTONS 8

#define READ_DELAY     2

#define WRITE_DELAY    10
#define MAX_SEQUENCE_LENGTH 10
#define MIN_SEQUENCE_LENGTH 6

#define NUMBER_OF_SEQ   6
#define SEQ1_LEN    11
#define SEQ2_LEN    6
#define SEQ3_LEN    7
#define SEQ4_LEN    7 
#define SEQ5_LEN    6
#define SEQ6_LEN    6

int wrongMatch_ = 0;

// Length of sequences.
int seq_length_[NUMBER_OF_SEQ] = { 
    SEQ1_LEN, SEQ2_LEN, SEQ3_LEN 
        , SEQ4_LEN, SEQ5_LEN, SEQ6_LEN
};

int seq1[SEQ1_LEN]   = { 3, 3, 3, 3, 3, 3, 3, 5, 0, 2, 3 };
int delay1[SEQ1_LEN] = { 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 1 };

int seq2[SEQ2_LEN]   = { 0, 0, 2, 0, 4, 3 };
int delay2[SEQ2_LEN] = { 1, 1, 1, 1, 1, 1 };

int seq3[SEQ3_LEN]   = { 4, 3, 2, 3, 2, 1, 2 };
int delay3[SEQ3_LEN] = { 1, 1, 1, 1, 1, 1, 1 };

int seq4[SEQ4_LEN]   = { 0, 0, 5, 5, 6, 6, 5 };
int delay4[SEQ4_LEN] = { 1, 1, 1, 1, 1, 1, 1 };

int seq5[SEQ5_LEN]   = { 3, 3, 3, 7, 6, 7 };
int delay5[SEQ5_LEN] = { 1, 1, 1, 1, 1, 1 };

int seq6[SEQ6_LEN]   = { 3, 2, 0, 3, 2, 0};
int delay6[SEQ6_LEN] = { 1, 1, 2, 1, 1, 1};

int* sequences_[NUMBER_OF_SEQ] = { seq1, seq2, seq3, seq4, seq5, seq6 };
int* delays_[NUMBER_OF_SEQ] = { delay1, delay2, delay3, delay4
    , delay5, delay6 };

#define THRESHOLD_FOR_BUTTON_PRESS  10

/**
 * @brief At each step it tracks which sequence is a poteintial match.
 */
double matched_seq_[NUMBER_OF_SEQ+1];

/**
 * @brief Which index is being matched now.
 */
int running_index_[NUMBER_OF_SEQ];
int n_button_press_ = 0;

/*  Running mean of signal. */
float running_mean_ = 0.0;

/*  List of buttons to get input from 
 *  PIN-13 is never a good idea as input/output pin
 */
int buttonList_[NUMBER_OF_BUTTONS] = { A0, A1, A2, A3, A4, A5, A6, A7 };

// This button reset the matching results. Everything starts from the begining.
#define RESET_BUTTON 7
#define NOTE_DURATION 300


/*-----------------------------------------------------------------------------
 *  Buzzer related
 *-----------------------------------------------------------------------------*/
// Pin at which buzzor is attached
#define BUZZER_PIN  9

// For each button assign a tone.
int buttonTones_[ ] = { 
    NOTE_C5, NOTE_CS5, NOTE_D5, NOTE_E5, NOTE_FS5
        , NOTE_G5, NOTE_A5, NOTE_B5
};



/**
 * @brief Input from button is stored here.
 */
int input_[3];

int num_of_buttons_pressed_ = 0;

/**
 * @brief Play a tone for button buttonId. Currently it plays by my
 * modulating the pulse width.
 *
 * @param i
 */
void playNote( int buttonId, long duration = 0 )
{
    //Serial.print( "Playing button " );
    //Serial.print( buttonId );
    //Serial.print( " Freq : " );
    //Serial.println( buttonTones_[ buttonId ] );
    if( duration == 0 )
        duration = NOTE_DURATION;
    tone( BUZZER_PIN, buttonTones_[buttonId], duration );
}

void resetMatchingResult( bool silent = true )
{
    Serial.println( "Reset sequence matching results" );
    n_button_press_ = 0;
    for (size_t i = 0; i < NUMBER_OF_SEQ; i++) 
    {
        matched_seq_[i] = 0.0;
        running_index_[i] = 0;
    }

    if( ! silent )
        playNote( NOTE_A1, 1000 );
}

// the setup routine runs once when you press reset:
void setup()
{
    // Setup up baud rate
    Serial.begin(19200);

    pinMode( BUZZER_PIN, OUTPUT );

    // Set the button to be read-only. 
    for (size_t i = 0; i < NUMBER_OF_BUTTONS; i++) 
        pinMode( buttonList_[i], INPUT );

    for (size_t i = 0; i < NUMBER_OF_SEQ; i++) 
        running_index_[i] = 0;

    for (size_t i = 0; i < 3; i++) 
        input_[i] = -1;


    /*-----------------------------------------------------------------------------
     *  Now setup LEDs 
     *-----------------------------------------------------------------------------*/
    strip.begin( );
    strip.show( );

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
        int val = analogRead( buttonList_[i] );
        sum = sum + pow(4, i) * val;
        //Serial.println( val );
        input_[i] = val; 
        delay(READ_DELAY);
    }
    return sum;
}

/**
 * @brief which button is pressed by user. If no button is pressed, it returns
 * -1.
 *
 * @return The index of button in buttonList_  if a button is pressed, -1
 * otherwise.
 */
int whichButtonIsPressed( void )
{
    int val = -1;
    for (size_t i = 0; i < NUMBER_OF_BUTTONS; i++) 
    {
        delay(READ_DELAY);
        val = analogRead( buttonList_[i] );
        if( val >= THRESHOLD_FOR_BUTTON_PRESS )
        {
            // Now wait of button release.
            // Wait for 500 ms for button release else continue.
            for (size_t ii = 0; ii < 500 / READ_DELAY; ii++) 
            {
                delay( READ_DELAY );
                val = analogRead( buttonList_[i] );

                if( val < THRESHOLD_FOR_BUTTON_PRESS )
                    return i;
            }
        }
    }
    return -1;
}

// This is for testing purpose.
void pressButton( unsigned int buttonId )
{
    // Press button no buttonId 
    pinMode( buttonList_[ buttonId ], OUTPUT );
    digitalWrite( buttonList_[ buttonId ], HIGH );
    delay( WRITE_DELAY );
    pinMode( buttonList_[ buttonId ], INPUT );
}

// prepend the pressed button value at the begining of input. Shift everyone
// else to right.
void addInput( int input )
{
    for (size_t i = 2; i > 0; i--) 
        input_[i] = input_[i-1];
    input_[0] = input;
}

void printArray( double* array, size_t size)
{
    Serial.print( " <" );
    for (size_t i = 0; i < size; i++) 
    {
        Serial.print( array[i] );
        Serial.print( "," );
        
    }
    Serial.print("> ");
}

void printIArray( int* array, size_t size)
{
    Serial.print( " |" );
    for (size_t i = 0; i < size; i++) 
    {
        Serial.print( array[i] );
        Serial.print( "," );
    }
    Serial.println(" |");
}

/**
 * @brief Get the maximum value from an array.
 *
 * @param array
 * @param arrayLen
 *
 * @return 
 */
double maxInDArr( double* array, int arrayLen )
{
    double maximum = 0.0;
    for (size_t i = 0; i < arrayLen; i++) 
        if(maximum > array[i])
            maximum = array[i];
    return maximum;
}

int maxInIArr( int* array, int arrayLen )
{
    int maximum = 0.0;
    for (size_t i = 0; i < arrayLen; i++) 
        if(maximum > array[i])
            maximum = array[i];
    return maximum;
}

void playSequece( int seqid )
{
    // Play sequence with id seq
    int* seq = sequences_[ seqid ];
    int seqLength = seq_length_[ seqid ];

    int duration = 300;

    delay( 1000 );
    for (size_t i = 0; i < seqLength; i++) 
    {
        playNote( seq[i], duration );
        delay( delays_[seqid][i] * duration );
    }
    delay( 1000 );
}

void matchSequences( void )
{
    n_button_press_ += 1;
    // At any time, the current button pressed is at input_[0]
    int currVal = input_[0];

    bool noneMatch = true;
    //Serial.print( "Running index ");
    //Serial.println( running_index_ );
    for (size_t i = 0; i < NUMBER_OF_SEQ; i++) 
    {
        if( currVal == sequences_[i][running_index_[i]] )
        {
            running_index_[i] += 1;
            matched_seq_[i] += 1.0;
            noneMatch = false;
        }
        else
            // when there is no match, decay every element to x% of its value.
            matched_seq_[i] *= 0.9;
    }

    /**
     * @param noneMatch
     *
     * @brief When noneMatch is true i.e. input is not part of any sequence, we
     * don't reset everything to zero. Rather decay everything to 90% of its
     * total value. We still print a character to indicate error.
     *
     */
    if( noneMatch )
    {
        Serial.print('x');
        wrongMatch_ += 1;
        if( wrongMatch_ > 5 )
        {
            resetMatchingResult( false );
            wrongMatch_ = 0;
        }
        int maxRunningIndex = maxInIArr( running_index_, NUMBER_OF_SEQ);
        if( n_button_press_ > 2 * MAX_SEQUENCE_LENGTH && 
                 maxInDArr( matched_seq_, NUMBER_OF_SEQ ) < MIN_SEQUENCE_LENGTH )
        {
            Serial.println( "Ha ha! It's better to restart now");
            resetMatchingResult( false );
        }
    }
    else
    {
        for (size_t i = 0; i < NUMBER_OF_SEQ; i++) 
        {
            if( running_index_[i] >= seq_length_[i] &&
                    matched_seq_[i] / running_index_[i] >= 0.7 )
            {
                // i'th sequence is matched.
                Serial.print( "\n|| Sequence matched." );
                Serial.println( i );
                playSequece( i );
                // Reset everything
                resetMatchingResult( true );
                break;
            }
        }
    }

    printArray( matched_seq_, NUMBER_OF_SEQ);
    //printIArray( running_index_, NUMBER_OF_SEQ);
    Serial.print( '\n' );
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
            Serial.print( buttonId );
            Serial.print( " " );
            //Serial.println( num_of_buttons_pressed_ );
            num_of_buttons_pressed_ += 1;
            num_of_buttons_pressed_ = num_of_buttons_pressed_ % NUMBER_OF_BUTTONS;
            addInput( buttonId );
            matchSequences();
        }

    }
}

// the loop routine runs over and over again forever:
void loop() 
{
    int buttonId = whichButtonIsPressed( );
    if( buttonId >= 0 )
    {
        //Serial.print( "Button pressed : " );
        //Serial.println( buttonId );
        //Serial.println( num_of_buttons_pressed_ );
        num_of_buttons_pressed_ += 1;
        num_of_buttons_pressed_ = num_of_buttons_pressed_ % NUMBER_OF_BUTTONS;
        addInput( buttonId );
        playNote( buttonId );
        lightupLED( buttonId );
        matchSequences();
    }

    // Send a simple pixel chase in...
    //colorChase(strip.Color(127,   0,   0), 50); // Red
    //colorChase(strip.Color(127, 127,   0), 50); // Yellow
    //colorChase(strip.Color(  0, 127,   0), 50); // Green
    //colorChase(strip.Color(  0, 127, 127), 50); // Cyan
    //colorChase(strip.Color(  0,   0, 127), 50); // Blue
    //colorChase(strip.Color(127,   0, 127), 50); // Violet

    //test( );
}
