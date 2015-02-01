# Berth

berth (\\ˈbərth\\): a place in the water near the shore where a ship stops and stays.

Berth is a tool to help you automate the building of packages for an array of operating system and package systems, while not putting a big load on the local dependencies where you build the packages. It does this by using a Docker container of your choice to build your project inside, and then use another container with the [FPM](https://github.com/jordansissel/fpm) package creator inside to package up the project.


## Installation

In order to use Berth you need to have Python and Docker installed. Berth has been tested with Python 2.7 and 3.4, and Docker version 1.4. If you are not running on a system where Docker runs, ie. Mac OS X, you can use [boot2docker](http://boot2docker.io/) instead. Berth will use the same environment variables as the `docker` command to figure out which Docker host to talk to.

When those requirements are in place, you can install Berth through `pip` with:

    pip install berth


## Usage

    $ berth --help
    Usage: berth [OPTIONS] <CONFIG FILE>

      Berth use Docker containers to build packages for you, based on a YAML
      configuration file.

    Options:
      --version      Show the version and exit.
      -v, --verbose  Turn on verbose output.
      -d, --debug    Turn on debug output.
      --help         Show this message and exit.

There's not much to specify on the command line, except for output level and a configuration file. The configuration file is in YAML format and will look something like the [sample.yaml](sample.yaml) file.


## Configuration

The configuration file has three possible sections, the first is the `environment` section where you can specify environment variables that will made available to the rest of this configuration. This means you only have to specify metadata once, ie. the version of the package you are building.

Next up is the `build` section, where you specify everything related to building the project. You can choose the Docker image you would like to do the build in, so if you ie. want to build a Go project, you can use the `golang` image and have any dependencies available you would need. You also specify the which volumes you would like to have mapped into the container, this can be used both for getting source files into the container but also to get built files out of it. Lastly you should specify a script to use for the build process. It will be executed as `/build-script`, meaning that it should contain an interpreter as the first line.

The last section of the configuration file is `package` which covers the packaging of the project. You can again specify which image you want to build with and which volumes you need to get mapped into the container, the only requirement to the image is that it has `fpm` in `$PATH`. The remainder of the `package` section is used to specify the options you want to pass to `fpm` for when it builds the package. The options will more or less be mapped directly into `fpm`, with a few exceptions:

- If the value is a boolean true to YAML, the key will be passed as a flag
- If the value is a list, the parameter will be passed multiple times, once for each item in the list
- If the key specified is either `template-value` or `deb-field`, the values will be mapped into `fpm` with the correct syntax
- If the key is `_arguments` it will be sent to `fpm` as the last arguments in the command, with no parameter specified before them

The list of parameters `fpm` accepts can either be found be running `fpm --help` or on [their wiki](https://github.com/jordansissel/fpm/wiki#usage).
