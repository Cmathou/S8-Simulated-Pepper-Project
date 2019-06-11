#!/usr/bin/env python

# based on http://doc.aldebaran.com/2-5/naoqi/core/altabletservice-api.html#ALTabletService::onTouchDown__qi::Signal:float.float:

import qi
import argparse
import sys
import time

def main(session):

    try:
        tabletService = session.service("ALTabletService")

        signalID = 0

        # test of onTouchDown signal from the tablet
        #  AND of showImage() and hideImage() methods
        #  depending on which part of the screen is touched, 
        #  display different images during 3s then hide them
        def callback(x, y):
            print "signal onTouchDown(" + str(x) + ", " + str(y) + ") received"
            xMax = 1280
            if (x < xMax/2):
                # left half of the screen
                tabletService.showImage("image_left.png")
            else:
                # right half of the screen
                tabletService.showImage("image_right.png")
            
            time.sleep(3)

            tabletService.hideImage()

        signalID = tabletService.onTouchDown.connect(callback)
        print "connected signal onTouchDown (" + str(signalID) + ")"

        # let it run for 30s
        time.sleep(30)

        tabletService.hideImage()

        tabletService.onTouchDown.disconnect(signalID)

    except Exception, e:
        print "Error: ", e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)