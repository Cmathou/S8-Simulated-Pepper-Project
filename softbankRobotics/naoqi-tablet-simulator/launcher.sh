#!/bin/bash

NAOQI_PORT=9559 # default port for naoqi

# shoud point to the dir containing qimessaging-json
QIMESSAGING_JSON_DIR="/home/tp/softbankRobotics/libqi-js"
NO_QIMESSAGING=0

while true; do
    case "$1" in
        "--naoqi-port") NAOQI_PORT=$2; shift 2;;
        "--qimessaging-json-dir") QIMESSAGING_JSON_DIR=$2; shift 2;;
        "--no-qimessaging") NO_QIMESSAGING=1; shift;;
        "-h" | "--help")
            echo "Naoqi Tablet Simulator - launcher script"
            echo "Usage : launcher.sh [--naoqi-port <port>] [--qimessaging-json-dir <dir>] [--no-qimessaging]"
            echo "              --naoqi-port                the port naoqi is listening to (default 9559)"
            echo "              --qimessaging-json-dir      the path to qimessaging-json script"
            echo "              --no-qimessaging            don't start qimessaging-json script"
            echo "              --help                      display this help"
            exit 0;;
    * ) break;;
    esac
done

if [ "$NO_QIMESSAGING" -eq 0 ]
then
    echo "starting qimessaging-json in background"
    $QIMESSAGING_JSON_DIR/qimessaging-json tcp://127.0.0.1:$NAOQI_PORT &
fi

echo "starting nts"
./nts.py --qi-url 127.0.0.1:$NAOQI_PORT # will terminate with ctrl+C

if [ "$NO_QIMESSAGING" -eq 0 ]
then
    kill %1 # qimessaging-json should be job [1]
fi

