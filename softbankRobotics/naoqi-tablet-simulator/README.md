# Naoqi tablet simulator

![licence](https://img.shields.io/badge/licence-MIT-brightgreen.svg?style=flat-square)
![version](https://img.shields.io/badge/version-0.5.1-yellow.svg?style=flat-square)

## Purpose

The purpose of this project is to provide a simulator to emulate the tablet fixed on Pepper's chest.

## Context

Pepper is a robot developed to interact with humans in different situations. It is able to recognize faces and speech, and speak to people. It is equipped with a tactile tablet that is used as a additional means of interaction.

When developing applications running on Pepper, one often needs to use a Pepper simulator on their machine, to make the development more convenient than using the physical robot. Several ways to simulate the robot behaviour exist (Choregraphe, RViz, Gazebo, Webots...), however, these simulators does not include management of the tablet. It seems that there is currently no solution available to emulate the robot's tablet.

In order to allow developers to have a little more complete Pepper simulation at their disposal, we need to develop a solution to emulate the tablet.

## Technically speaking : the ALTabletService

The idea is to replace the `ALTabletService` used in the physical robot to control the tablet. Indeed, when using the physical robot, this service exists and is called by the modules of the application (and Naoqi) to control the tablet ; however, when using a simulator, the `ALTabletService` does not exist, and all calls to any method of this service will fail.

So, we create a new service with the same name, which will be run when using a simulator on a local computer. It must contain exactly the same methods as the original `ALTabletService`, and will be registered as a service in a running Naoqi instance. Instead of failing, the Naoqi modules and application modules will call the methods of the substitute service.

All `ALTabletService` methods must be implemented, and must return at least an acceptable value by the requesting module.

## The Code

The main program, replacing ALTabletService, is written in Python.

The web part, used in a browser to display the simulated tablet screen, is written in HTML/CSS with javascript and JQuery.

## Try it out

You can test a small testing version of the program (that was originally the proof-of-concept, version 0.1.0) with a little script `test.py` :

1. First of all, you need to have a running instance of Naoqi.
2. Copy `config/config.template.yml` to `config.yml`, preferably without changing the default values.
3. Run `nts.py` which is the main program. It will run for 30s before stopping.
4. Open or reload `web/page.html` in your browser. It will connect to `nts.py` which runs a websocket server.
5. Run `examples/test.py`. Its precise behavior is described by comments in the script, and it will run for 30s.
6. Test the program by clicking on the left or right side of the web tablet.

## Install

Detailed installation instructions can be found [here](https://gitlab.com/davidvivier/naoqi-tablet-simulator/wikis/Installation).

## Documentation

You can read the documentation at the [project wiki](https://gitlab.com/davidvivier/naoqi-tablet-simulator/wikis/home). (work in progress)

## License

This project is currently published under the MIT License.

If we need to use external libraries (with other licences) in the future, we might be led to switch to a less permissive licence ; nevertheless, we have strong intention to keep this project remaining free software ("free" as in "freedom") and will be very careful about it.

The Free Software Definition on gnu.org : [https://www.gnu.org/philosophy/free-sw.en.html](https://www.gnu.org/philosophy/free-sw.en.html)

## Versioning

This project uses [Semantic Versioning](https://semver.org/), and here is the the [changelog](CHANGELOG.md) .

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Feedback

Feel free to try the program out (at your own risk) and add issues to signal bugs or suggest improvements, and let us know if the documentation is erroneous or insufficient.

Contact email address: [dev@davidvivier.fr](mailto:dev@davidvivier.fr)

## Notes

This is an early-stage project, we consider it being an alpha version. Not all necessary methods are implemented. Use at your own risk.

The name of the project and program is subject to change. Besides, at this stage, we are not sure if this project should be called a "simulator" or rather an "emulator".

This project was started as an end-of-studies project at CPE Lyon engineering school, France.

The proof-of-concept of the project was published on January, 9th 2019.
