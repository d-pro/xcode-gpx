#!/usr/bin/python
# Python 2.7

'''
    This is free and unencumbered software released into the public domain.
    Anyone is free to copy, modify, publish, use, sell, or distribute this 
    software for any purpose, commercial or non-commercial, and by any means.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
'''

################################################################################

# This script will loop through current direcory and convert all *.gpx files
# created by handheld gps devices into *-.gpx files, which can use as Location
# Simulator for Xcode.
#
# Tested with Garmin Edge 500 and Xcode 7.2

################################################################################

import os

# get list of files in current dir
files = os.listdir(os.curdir)

for fileName in files:
    
    # loop through all gpx files, but skip -xc.gpx files
    if '.gpx' in fileName and '-xc.gpx' not in fileName and '._' not in fileName:
        
        # open file and check if content meet requirements
        file = open(fileName, 'r')

        skipTheFile = 1
        for line in file:
            if '<trkpt' in line and 'lat' in line and 'lon' in line and '>' in line:
                skipTheFile = 0
                break
        # if nothing to convert, go to next file
        if skipTheFile == 1:
            file.close()

        else:
            # create name for output file
            outputFileName = fileName.replace('.gpx', '-xc.gpx')
            file = open(outputFileName, 'a')

            # write new gpx header
            file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?> \n <gpx \n xmlns="http://www.topografix.com/GPX/1/1" \n xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \n xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" \n version="1.1" \n creator="xcode-gpx.py github:d-pro/xcode-gpx"> \n')

            # read file as list of lines
            inputLines = open(fileName, 'rU')
            outputLines = []
            
            # loop through all lines
            wptOpen = 0
            error = 0
            for line in inputLines:
                
                # replace point type: <trkpt -> wpt
                if '<trkpt' in line and 'lat' in line and 'lon' in line and '>' in line:

                    # replace tag
                    if wptOpen == 0:
                        wptOpen = 1
                        line = line.replace('trkpt', 'wpt')
                        file.write(line)
                    
                    # or abort if previous tag dont't closed and delete non-completed file
                    else:
                        print 'file', fileName, 'structure corrupted'
                        file.close()
                        os.remove(outputFileName)
                        error = 1
                        break

                # use point timestamp as point name
                if wptOpen == 1 and '<time>' in line and '</time>' in line:
                    wptOpen = 0
                    line = line.replace('<time>', '<name>')
                    line = line.replace('</time>', '</name> </wpt>')
                    file.write(line)
        
            # close the gpx tag and close the file
            if error == 0:
                file.write('</gpx>')
                file.close()
                print 'created:', outputFileName
print 'done'