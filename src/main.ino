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

/**
 * @brief Keep the running values of signal.
 */
int signal_[WINDOW_SIZE];

/*  Running mean of signal. */
float running_mean_ = 0.0;

double computeMean(  )
{
    double sum = 0.0;
    for (size_t i = 0; i < WINDOW_SIZE; i++) 
        sum += signal_[i];
    running_mean_ = sum / WINDOW_SIZE;
    return running_mean_;
}

void appendToSignal( int sensorValue )
{
    for (size_t i = 0; i < WINDOW_SIZE - 1; i++) 
        signal_[i] = signal_[i+1];
    signal_[WINDOW_SIZE-1] = sensorValue;
}

// the setup routine runs once when you press reset:
void setup()
{
    // initialize serial communication at 9600 bits per second:
    Serial.begin(19200);

    pinMode( A2, OUTPUT );
    pinMode( 13, OUTPUT );

    digitalWrite( A2, HIGH );

    pinMode( A1, OUTPUT );
    digitalWrite( A1, LOW );

    /* Initialize signal  */
    for (size_t i = 0; i < WINDOW_SIZE; i++) 
        signal_[i] = 10;

}

// the loop routine runs over and over again forever:
void loop() 
{
    // read the input on analog pin 0:
    int sensorValue = analogRead(A0);
    appendToSignal( sensorValue );
    computeMean( );

#if 0
    for (size_t i = 0; i < WINDOW_SIZE; i++) 
    {
        Serial.print( signal_[i] );
        Serial.print( ' ' );
    }
#endif

    Serial.print( sensorValue );
    Serial.print( ' ' );
    Serial.print( running_mean_ );
    Serial.print( '\n' );
    if( sensorValue > (1.1 * running_mean_) )
    {
        Serial.println( "Trigger" );
        for (size_t i = 0; i < 5; i++) 
        {
            digitalWrite( 13, HIGH );
            delay( 30 );
            digitalWrite( 13, LOW);
            delay( 30 );
            
        }
    }
    digitalWrite( 13, LOW );
    delay(1); 
}
