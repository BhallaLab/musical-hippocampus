#!/bin/bash - 
#===============================================================================
#
#          FILE: run.sh
# 
#         USAGE: ./run.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: 08/31/2016 03:43:25 PM
#      REVISION:  ---
#===============================================================================

set -e
make upload
set -o nounset                              # Treat unset variables as an error
miniterm.py -p /dev/ttyACM0 -b 19200 
