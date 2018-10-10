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

#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

string winName_ = "Hippo";

size_t w_ = 800;
size_t h_ = 480;


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
    namedWindow( winName_, 0 );
    while(true)
    {
        random_color( img_ );
        imshow( winName_, img_ );
        waitKey(1);
    }
    destroyAllWindows();
}
