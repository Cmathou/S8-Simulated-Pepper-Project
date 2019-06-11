#!/usr/bin/env python

import Queue
import threading

import qi

import time

import tornado.ioloop
import tornado.websocket
import json

import yaml

import webbrowser

# https://stackoverflow.com/questions/1843422/get-webpage-contents-with-python
from six.moves import urllib 

config = yaml.safe_load(open("config/config.yml"))
# TODO check if config file is valid
# TODO allow to override config file with script parameters

app = None

queueSW = None
queueWS = None

waiting_return = {}

def debug(msg):
    # print only if verbose
    if config['verbose']:
        print msg

class ALTabletService:
    
    robot_ip = config['robot_ip']

    # the path we need to replace, can be specific to the simulator used
    dir_to_replace = config['path_correction']['dir_to_replace']
    # the path (relative to the page.html file) 
    replace_with = config['path_correction']['replace_with']

    # signals
    onTouchDown = None
    onTouchUp = None

    ## Variables that are normally at the robot tablet level


    # Tablet Modes
    MODE_SLEEP = 0
    MODE_IMAGE = 1
    MODE_VIDEO = 2
    MODE_WEBVIEW = 3

    tabletMode = MODE_SLEEP

    onTouchScaleFactor = 1.0

    webview_url = None

    # waiting_return = {}
    last_call_id = -1

    def __init__(self):
        debug("__init__ in ALTabletService")
        self.onTouchDown = qi.Signal("m", self.onTouchDownSignal_connect)
        self.onTouchUp = qi.Signal("m", self.onTouchUpSignal_connect)

    def onTouchDownSignal_connect(self, c):
        debug("onTouchDownSignal_connect (" + str(c) + ")")
    
    def onTouchDownSignal_trigger(self, args):
        debug("triggering onTouchDownSignal(" + str(args) + ")")
        self.onTouchDown(args[0], args[1])

    def onTouchUpSignal_connect(self, c):
        debug("onTouchUpSignal_connect(" + str(c) + ")")
    
    def onTouchUpSignal_trigger(self, args):
        debug("triggering onTouchUpSignal(" + str() + ")")
        self.onTouchUp(args[0], args[1])

    # array of trigger method for each signal
    triggerMethods = {
        "onTouchDown":onTouchDownSignal_trigger,
        "onTouchUp":onTouchUpSignal_trigger
    }

    # this method is called when receiving a signal from the client interface
    #   -> call the appropriate trigger method to actually activate 
    #       the corresponding signal of our ALTabletService 
    def triggerSignal(self, signal, args):
        debug("triggerSignal(" + signal + ", " + str(args))
        self.triggerMethods[signal](self, args)

    # when using a simulator, the resource files (images) are not at the same location
    # as when using the real robot. So we need to correct this path.
    # This is done with correct_path() and with parameters dir_to_replace and replace_with.

    def correct_path(self, path):
        if config['path_correction']['enable']:
            if (path.find(self.robot_ip) >= 0 and path.find(self.dir_to_replace) >= 0):
                debug("Correcting path : " + path)
                path = path.replace('http://', '')
                path = path.replace('https://', '')
                path = path.replace(self.robot_ip, '')
                path = path.replace(self.dir_to_replace, self.replace_with)
                debug("Corrected path  : " + path)
        return path

    ##  ALTabletService normal methods

    # Webview methods 

    def cleanWebview(self):
        debug("in simulation ALTabletService : cleanWebview()")
        self.webview_url = None
        self.tabletMode = self.MODE_SLEEP
        self.callMethod("cleanWebview")

    
    def hideWebview(self):
        debug("in simulation ALTabletService : hideWebview()")
        self.tabletMode = self.MODE_SLEEP
        return_value = self.callMethod("hideWebview")
        return return_value

    def loadApplication(self, name):
        debug("in simulation ALTabletService : loadApplication(" + name + ")")
        host = config["websocket_server"]["host"]
        port = str(config["websocket_server"]["port"])
        url = "http://" + host + ":" + port + "/app/" + name + "/html/index.html"

        return_value = self.loadUrl(url)
        return return_value

    def loadUrl(self, url):
        debug("in simulation ALTabletService : loadUrl(" + url + ")")
        self.webview_url = url
        return_value = self.callMethod("loadUrl", [url])
        return return_value

    def showWebview(self, *path):
        # using path=None (to use None as default argument if no argument is passed to showWebview) 
        #   does not work ("RuntimeError : Arguments types did not match for showWebview()" )
        # so instead, we use "arbitrary arguments" then check if a path was passed or not.
        # According to Philippe D. (from Aldebaran) in 2014, "default arguments are not supported anymore"
        #   (see https://community.ald.softbankrobotics.com/ja/node/1245)
        debug("in simulation ALTabletService : showWebview(" + str(path) + ")")
        if path:
            self.loadUrl(path[0])
        self.tabletMode = self.MODE_WEBVIEW
        return_value = self.callMethod("showWebview")
        return return_value

    # Video

    def getVideoLength(self):
        debug("in simulation ALTabletService : getVideoLength()")
        value = self.callMethod("getVideoLength")
        return value

    def getVideoPosition(self):
        debug("in simulation ALTabletService : getVideoPosition()")
        value = self.callMethod("getVideoPosition")
        return value

    def pauseVideo(self):
        debug("in simulation ALTabletService : pauseVideo()")
        return_value = self.callMethod("pauseVideo")
        return return_value

    def playVideo(self, url):
        debug("in simulation ALTabletService : playVideo(" + url + ")")
        return_value = self.callMethod("playVideo", [url])
        return return_value
    
    def resumeVideo(self):
        debug("in simulation ALTabletService : resumeVideo()")
        return_value = self.callMethod("resumeVideo")
        return return_value

    def stopVideo(self):
        debug("in simulation ALTabletService : stopVideo()")
        return_value = self.callMethod("stopVideo")
        return return_value
    
    # Image
    
    def hideImage(self):
        debug("in simulation ALTabletService : hideImage()")
        return_value = self.callMethod("hideImage")
        return return_value

    def setBackgroundColor(self, color):
        debug("in simulation ALTabletService : setBackgroundColor(" + color + ")")
        self.callMethod("setBackgroundColor", [color])

    def showImage(self, path):
        debug("in simulation ALTabletService : showImage(" + path + ")")
        path = self.correct_path(path)
        return_value = self.callMethod("showImage", [path])
        return return_value
      


    

    # generic method, that will transmit each specific method call to the client
    def callMethod(self, method, args = None):
        debug("in callMethod('" + method + "')")
        global queueSW
        global waiting_return

        # generate a new call_id (increment the previous one) 
        # the call_id is used to manage the multiple calls between the server and client
        print "previous id=" + str(self.last_call_id)
        self.last_call_id += 1
        call_id = self.last_call_id
        jsonString = json.dumps({"method":method, "args":args, "call_id":call_id})
        debug("call_id = " + str(call_id))
        debug("init waiting_return[" + str(call_id) + "] = None")
        waiting_return[call_id] = None

        # send to client
        queueSW.put(jsonString)
        
        print("waiting in " + str(self))
        debug("waiting for waiting_return[" + str(call_id) + "]")
        while (waiting_return[call_id] == None):
            #wait for the return value 
            # print str(waiting_return[call_id])
            pass
        #we have the value
        debug("Returning value " + str(waiting_return[call_id]))
        return waiting_return[call_id]
        

    # ALTabletService methods with specific behaviour because of the simulation

    def getOnTouchScaleFactor(self):
        """
            From ALTabletService doc : Get the touch scale factor of current view displayed. Default is 1.0 for all views except for the browser view which is 1.34 .
        """
        if (self.tabletMode == self.MODE_WEBVIEW):
            return 1.34
        return self.onTouchScaleFactor

    def setOnTouchWebviewScaleFactor(self, scaleFactor):
        debug("in simulation ALTabletService : setOnTouchWebviewScaleFactor(" + scaleFactor + ")")
        self.onTouchScaleFactor = scaleFactor

    def robotIp(self):
        return self.robot_ip

class ServiceThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        global app
        debug("Running ServiceThread")
        app = qi.Application()
        try:
            app.start()
        except RuntimeError:
            print ("RuntimeError when launching qi Application for ALTabletService - Is the naoqi instance running and accessible ?")
            global queueSW
            queueSW.put("quit")
            return
        
        session = app.session
        service = ALTabletService()
        session.registerService("ALTabletService", service)
        debug("Starting ALTAbletService in ServiceThread")
        app.run()

        debug("Service thread exiting")

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    # TODO restrict to only one client 

    instance = None

    def check_origin(self, a):
        return True
    
    def open(self):
        debug("previous instance was " + str(WebSocketHandler.instance))
        remote_ip = self.request.remote_ip
        
        if (WebSocketHandler.instance != None):
            # there was already a client connected

            # behavior depends on configuration
            if config['replace_connection']:
                print "Closing previous connection to " + remote_ip 
                WebSocketHandler.instance.close()
            else:
                self.close()
                print "Connection to " + remote_ip + " cancelled because another client is connected"
                return
        
        # remember the instance
        WebSocketHandler.instance = self 
        debug("WebSocket opened (" + remote_ip + ")")

    @classmethod
    def send_message(self, msg):
        debug("in WebSocketHandler.send_message(" + msg + ")")
        if self.instance:
            self.instance.write_message(msg)

    def on_message(self, message):
        debug("(on_message) Received : " + message)

        global queueWS

        # data is supposed to be JSON here
        #TODO maybe add specific value in payload to check data integrity ?
        try:
            data = json.loads(message)
            msgType = data['type']
            if (msgType == "signal"):
                self.signalReceived(data['signal'], data['args'])
                queueWS.put(data)
            elif (msgType == "return"):
                queueWS.put(data)
            elif (msgType == "info"):
                self.infoReceived(data["info"], data['args'])
            else:
                print("Error : received message of unknown type : " + msgType)
                return 1
        except ValueError:
            print("Error : Not valid JSON format")
        else:
            pass

    def signalReceived(self, signal, args):
        debug("signalReceived " + signal + str(args))

    def infoReceived(self, info, args):
        debug("infoReceived " + info + args)

    def on_close(self):
        debug("WebSocket closed (" + self.request.remote_ip + ")")

class WebviewRequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
    
    def get(self, resource):
        debug("in WebviewRequestHandler.get(" + resource + ")")
        #TODO case when resource is file:// ?
        webpage = urllib.request.urlopen(resource)
        
        # result depending on status code
        # TODO also treat case when status = 3xx (redirect)
        if (webpage.getcode() == 200):
            # write back the page to the client, that's what we want
            self.write(webpage.read())
        else:
            # return the received status code
            self.set_status(webpage.getcode())
        
        self.flush()
        self.finish()

class AppRequestHandler(tornado.web.RequestHandler):
    def initialize(self, type):
        self.type = type
    
    def get(self, resource):
        debug("in AppRequestHandler.get(" + resource + ")")
        
        if (self.type == "app"):
            # here we serve the application
            app_dir = config["applications"]["directory"]
            page = open(app_dir + "/" + resource)
        elif (self.type == "libs"):
            # and here we serve the libs
            lib_path = config["applications"]["lib"]
            page = open(lib_path)
        
        self.write(page.read())
        self.flush()
        self.finish()



class WebsocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        debug("Running WebsocketThread")

        websocket_app = tornado.web.Application([
                            #TODO maybe pass signal and params as arguments ? (simpler)
                            (r"/signal", WebSocketHandler),
                            (r"/webview/(.*)", WebviewRequestHandler),
                            (r"/app/(.*)", AppRequestHandler, dict(type="app")),
                            (r"/libs/(.*)", AppRequestHandler, dict(type="libs")),
                        ])
        port = config['websocket_server']['port']
        websocket_app.listen(port)
        debug("Websocket server is starting on port " + str(port))
        tornado.ioloop.IOLoop.current().start()

        debug("Websocket thread exiting")
    


class MainThread(threading.Thread):

    global queueSW
    global queueWS

    global waiting_return


    queueSW = Queue.Queue()
    queueWS = Queue.Queue()

    webSocketWorker = WebsocketThread()
    webSocketWorker.start()

    serviceWorker = ServiceThread()
    serviceWorker.start()

    # if we want the web tablet to be opened at startup
    if (config['auto_open_web_tablet'] == True):
        # wait a bit to give the webserver a chance to be up
        #  before the web tablet loads and initiates the connection
        time.sleep(1)
        webbrowser.open_new_tab('web/page.html')



    start_time = time.time()

    # TODO implement stop feature
    while time.time() - start_time < 300:

        try:
            # non-blocking get
            msg = queueWS.get(False)
            if isinstance(msg, str) and msg == "quit":
                break
            
            debug("Main thread : received " + str(msg) + " by queueWS")

            data = msg
            if (data["type"] == "signal"):
                # it's a signal
                signal = data["signal"]
                args = data["args"]
                app.session.service("ALTabletService").triggerSignal(signal, args)
            elif (data["type"] == "return"):
                # it's a return value of a method call
                if "value" in data:
                    value = data["value"]
                    call_id = data["call_id"]
                    print("got returned value (" + str(call_id) +"): " + str(value))
                    # give the value to the hungry called method that was waiting for it
                    waiting_return[call_id] = value
                else:
                    # for some reason, there is no value received
                    debug("Return packet received, but no value returned")
                    # we still unblock the waiting method
                    call_id = data["call_id"]
                    waiting_return[call_id] = -1
        
        except Queue.Empty:
            # nothing is received
            pass
        
        try:
            # non-blocking get
            msg = queueSW.get(False)
            if isinstance(msg, str) and msg == "quit":
                break
            
            debug("Main thread : received " + str(msg) + " by queueSW")
            WebSocketHandler.send_message(msg)
        
        except Queue.Empty:
            # nothing is received
            pass
        

    debug("Main thread exiting")

    app.stop()
    tornado.ioloop.IOLoop.current().stop()
    webSocketWorker.join()
    serviceWorker.join()

    exit(0)



if __name__ == '__main__':
    MainThread()
