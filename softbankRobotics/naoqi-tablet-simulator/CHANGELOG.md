# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2019-04-09

### Added

- More functions return a value (see 4aad7f)

### Changed

- nts.py stops after 5 minutes instead of 30 seconds (this time limit exists in case the script is stuck and cannot be stopped)
- Connection status is now at the top of the page, not below the tablet, so it is easier to see

### Fixed

- Corrected tornado behaviour (403 error when trying to connect from client)
- Config parameter `auto_open_web_tablet` was not taken into account

## [0.5.0] - 2019-03-13     `What do you mean, the methods return nothing ?`

### Added

- `ALTabletService` methods can now return a value, depending on the result (often client-side) of the method call, and theoretically corresponding to the expected behaviors described in the Naoqi documentation for ALTabletService.
- `getVideoLength()` and `getVideoPosition()` methods

### Fixed

- Small corrections and improvements

## [0.4.0] - 2019-01-28     `Don't you need a launcher ?`

### Added

- Launcher script `launcher.sh` which handles starting `qimessaging.json` in background and `nts.py`, with the correct arguments for each program

### Changed

- Created `AppRequestHandler` to handle application-related requests : the application files will be requested from the new `AppRequestHandler`, and not directly from files (details in commit db96c04). Basically, this removes the need for the user to adapt qimessaging.js path in the app's html file.
- `test` directory renamed to `examples` because it's more appropriate (`test.py` script is an example, not an unit test)

### Fixed

- Missing entry in configuration

## [0.3.0] - 2019-01-23     `Here comes the application`

### Added

- application support (launched by `loadApplication()` method) 

### Changed

- web page is loaded directly by the iframe, not passing through the webserver

### Fixed

- Image and video are now centered on the tablet (Issue #1)
- `Connect` and `Default` connection buttons work on the web client

## [0.2.0] - 2019-01-19     `Webview era`

### Added

- Webview management : Request handler specific for retreiving and serving webpages
- `showWebview()`, `hideWebview()`, `loadUrl()`, `cleanWebview()` methods
- `playVideo()`, `pauseVideo()`, `resumeVideo()`, `stopVideo()` methods
- `setBackgroundColor()` method
- `onTouchUp` qi signal

### Changed

- Only one instance of the main websocket handler (between the client and python script)
- Reorganize directory tree (`config/`, `doc/`, `test/`)

## [0.1.0] - 2019-01-09     `Proof-of-Concept`

### Added

- Proof-of-concept of the program
- `ALTabletService` is replacing the service of the same name in the physical robot
- `showImage()` and `hideImage()` methods 
- `onTouchDown` qi signal 
- Web interface to simulate the tablet
- Websocket between the web interface and the main Python program
- Threading and queues
