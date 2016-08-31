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
#define NUMBER_OF_SEQ   3
#define MAX_SEQUENCE_LENGTH 10

#define SEQ1_LEN    6
#define SEQ2_LEN    7
#define SEQ3_LEN    11

// Length of sequences.
int seq_length_[NUMBER_OF_SEQ] = { SEQ1_LEN, SEQ2_LEN, SEQ3_LEN };

int seq1[SEQ1_LEN] = { 0, 1, 2, 3, 4, 5 };
int seq2[SEQ2_LEN] = { 0, 1, 0, 0, 2, 2, 3 };
int seq3[SEQ3_LEN] = { 1, 1, 1, 0, 0, 0, 2, 2, 2, 3, 1 };
int* sequences_[NUMBER_OF_SEQ] = { seq1, seq2, seq3 };

/**
 * @brief At each step it tracks which sequence is a poteintial match.
 */
int matched_seq_[NUMBER_OF_SEQ+1];

/**
 * @brief Which index is being matched now.
 */
int running_index_ = 0;

/*  Running mean of signal. */
float running_mean_ = 0.0;

/*  List of buttons to get input from 
 *  PIN-13 is never a good idea as input/output pin
 */
int buttonList_[NUMBER_OF_BUTTONS] = { 6, 7, 8, 9, 10, 11 };

/**
 * @brief Input from button is stored here.
 */
int input_[3];

int num_of_buttons_pressed_ = 0;

void resetMatchingResult( )
{
    Serial.println( "Reset sequence matching results" );
    for (size_t i = 0; i < NUMBER_OF_SEQ; i++) 
        matched_seq_[i] = 0;
    running_index_ = 0;
        
}

// the setup routine runs once when you press reset:
void setup()
{
    // initialize serial communication at 9600 bits per second:
    Serial.begin(19200);

    // Set the button to be read-only. 
    for (size_t i = 0; i < NUMBER_OF_BUTTONS; i++) 
        pinMode( buttonList_[i], INPUT );

    for (size_t i = 0; i < 3; i++) 
        input_[i] = -1;

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

// prepend the pressed button value at the begining of input. Shift everyone
// else to right.
void addInput( int input )
{
    for (size_t i = 2; i > 0; i--) 
        input_[i] = input_[i-1];
    input_[0] = input;
}

void printArray( int* array, size_t size)
{
    Serial.print( "<" );
    for (size_t i = 0; i < size; i++) 
    {
        Serial.print( array[i] );
        Serial.print( "," );
        
    }
    Serial.println(">");
}

void matchSequences( void )
{
    // At any time, the current button pressed is at input_[0]
    int currVal = input_[0];

    bool noneMatch = true;
    //Serial.print( "Running index ");
    //Serial.println( running_index_ );
    for (size_t i = 0; i < NUMBER_OF_SEQ; i++) 
    {
        if( currVal == sequences_[i][running_index_] )
        {
            matched_seq_[i] += 1;
            noneMatch = false;
        }
        else
            matched_seq_[i] += 0;
    }
    if( noneMatch )
    {
        Serial.print('x');
        running_index_ = 0;
        for (size_t i = 0; i < NUMBER_OF_SEQ; i++) 
            matched_seq_[i] = 0;
        return;
    }
    else
    {
        running_index_ += 1;
        for (size_t i = 0; i < NUMBER_OF_SEQ; i++) 
        {
            if( matched_seq_[i] == seq_length_[i] )
            {
                Serial.print( "\n|| Sequence matched: " );
                Serial.println( i );
                // Reset everything
                resetMatchingResult( );
                break;
            }
        }
    }

    //printArray(matched_seq_, NUMBER_OF_SEQ);
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
        else if( buttonId == 9 )
            resetMatchingResult( );

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
