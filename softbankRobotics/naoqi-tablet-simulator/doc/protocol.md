# Communication protocol between tablet server and client

## Introduction

This document is part of the Naoqi Tablet Simulator project and describes the communication protocol specified between the two main parts of the project. It is supposed to be abstracted from the websocket implementation used either side.

## Context and naming

The word "Server" refers to the python script, which has to replace `ALTabletService`, and includes a websocket server.
The word "Client" refers to the web interface, on the other end of the websocket, which shows the tablet simulation, alongside a control panel.

The interaction between Server and Client is based on the `ALTabletService` API :
http://doc.aldebaran.com/2-5/naoqi/core/altabletservice-api.html

## From Server to Client

The messages typically sent by the server to the web interface are the methods called by the Naoqi modules : `showImage()`, `showWebView()`, `executeJS()`, etc.

They are transmitted using JSON and must follow this template : 

```json
{
    "type":"method",
    "method":"methodName",
    "args":["args", "passed", "to", "method"]
}
```

Example with a call to the showImage() method :

```json
{
    "type":"method",
    "method":"showImage",
    "args":["/path/to/image"]
}
```

## From Client to Server

The messages sent by the Client to the Server can be of two types :

* Event signals (`onTouchDown`, `onJSEvent`, etc)
* Information and controls from the web interface control panel

These messages also are transmitted using JSON, and must follow this template : 

```json
{
    "type":"signal",
    "signal":"signalName",
    "args":["args", "for", "this", "signal"]
}
```

As you see, the type of message (`signal` or `info`) is precised in the message data.

An example with the signal `onTouchDown` :

```json
{
    "type":"signal",
    "method":"onTouchDown",
    "args":[345, 159]
}
```


