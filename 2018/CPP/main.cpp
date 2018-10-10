/*
 * =====================================================================================
 *
 *       Filename:  main.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  Wednesday 10 October 2018 03:40:19  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 * =====================================================================================
 */

#include <iostream>
#include <string>
#include <iomanip>
#include <sstream>
#include <ctime>

#include <opencv2/opencv.hpp>
#include "config.hpp"

using namespace std;
using namespace cv;

Mat img_ = Mat::zeros(w_, h_, CV_8UC1);

void random_color( Mat& image )
{
    for (int i = 0; i < image.rows; i++)
    {
        for (int j = 0; j < image.cols; j++)
        {
            image.at<Vec3b>(i,j)[0] = rand()%255;
            image.at<Vec3b>(i,j)[1] = rand()%255;
            image.at<Vec3b>(i,j)[2] = rand()%255;
        }
    }
}

int main( int argc, char** argv)
{
    namedWindow( WINNAME, 0 );
    double t=0;
    time_t t0;

    size_t nFrames = 0;
    while(true)
    {
        nFrames += 1;
        t0 = time(0);
        random_color( img_ );
        //imshow( WINNAME, img_ );
        //waitKey(1);
        t += (time(0) - t0);
        if( nFrames % 20 == 0 )
            cout << "Current frame rate : " << (double) nFrames / t << endl;
    }
    destroyAllWindows();
}
