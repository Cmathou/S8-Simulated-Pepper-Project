# TODO

- Consult skilled people working with Pepper robots and familiar with Naoqi
- Write documentation (overview, architecture, threads, queues, protocol)
- Implement all `ALTabletService` methods
- Replace all `ALTabletService` signals
- Improve web interface (control panel)
- Improve config file management
- Manage cache for images
- manage resolution 1708x1067
- Ensure script is fully compatible with both pyhton2 and python3 (currently python2)
- Include reverse proxy in python web server to simplify setup
- Try to remove the need for a reverse proxy
- Reorganize classes into different files

## Methods of ALTabletService remaining to be implemented

http://doc.aldebaran.com/2-5/naoqi/core/altabletservice-api.html

````
    ALTabletService::executeJS()
    ALTabletService::getOnTouchScaleFactor()
    ALTabletService::loadApplication()
    ALTabletService::reloadPage()
    ALTabletService::setOnTouchWebviewScaleFactor()
    ALTabletService::getVideoLength()
    ALTabletService::getVideoPosition()
    ALTabletService::pauseGif()
    ALTabletService::preLoadImage()
    ALTabletService::resumeGif()
    ALTabletService::showImageNoCache()
    ALTabletService::hideDialog()
    ALTabletService::showAlertView()
    ALTabletService::showInputDialog()
    ALTabletService::showInputTextDialog()
    ALTabletService::configureWifi()
    ALTabletService::connectWifi()
    ALTabletService::disableWifi()
    ALTabletService::disconnectWifi()
    ALTabletService::enableWifi()
    ALTabletService::forgetWifi()
    ALTabletService::getWifiStatus()
    ALTabletService::getBrightness()
    ALTabletService::getAvailableKeyboards()
    ALTabletService::getWifiMacAddress()
    ALTabletService::goToSleep()
    ALTabletService::hide()
    ALTabletService::resetTablet()
    ALTabletService::robotIp()
    ALTabletService::setBrightness()
    ALTabletService::setKeyboard()
    ALTabletService::setTabletLanguage()
    ALTabletService::setVolume()
    ALTabletService::turnScreenOn()
    ALTabletService::version()
    ALTabletService::wakeUp()
    ALTabletService::getLastVideoErrorLog()
    ALTabletService::getCurrentLifeActivity()
    ALTabletService::postEventToApplication()
    ALTabletService::resetToDefaultValue()
````

## Signals of ALTabletService remaining to be replaced

````
    ALTabletService::onTouchDownRatio
    ALTabletService::onTouchMove
    ALTabletService::onConsoleMessage
    ALTabletService::onJSEvent
    ALTabletService::onPageFinished
    ALTabletService::onPageStarted
    ALTabletService::videoFinished
    ALTabletService::videoStarted
    ALTabletService::onImageLoaded
    ALTabletService::onInputText
    ALTabletService::onLoadPageError
    ALTabletService::onWifiStatusChange
    ALTabletService::onTouch
````

