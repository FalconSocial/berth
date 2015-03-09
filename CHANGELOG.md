# Berth Changelog

## 1.3.0 - 2015-03-09
* Added `--build-only` and `--package-only` flags to tell Berth to only do one of the two steps. This can be useful when setting up a configuration for a new package together with:
* New `--keep-containers` flag which makes the containers Berth create stay around after the jobs have ran. This will make you able to `docker run` them afterwards and inspect the files inside of them.
* Berth now provides streaming output of the build scripts if either the verbose or debug output levels are enabled, instead of only getting the output when the container stops.
* When builds took longer time to execute than 100 seconds, the run time of the container was outputtet in scientific format, this has now been corrected so it will always be outputtet as the number of seconds with 1 digit precision.

## 1.2.0 - 2015-02-12
* Made the "build" part of the configuration optional so you also can use Berth to just build Python and Ruby packages directly, since FPM supports that as input.

## 1.1.0 - 2015-02-01
* Enable the use of environment variables during build and packaging steps. This makes it easier to create an updated package by just increasing the version number one place.
* When a local path specified as a source for a volume doesn't exist, we now try to create a directory at that path and make use of that. If the directory creation fails then we complain like before.
* Minor improvements to configuration file checks.

## 1.0.1 - 2015-01-29
* Stop the package generation flow if the build script fails (exits with non-zero exit code)
* Disable hostname verification for Docker client, since the hostname and certificate doesn't match when using boot2docker - Fig does this as well
* Place the build script file in the current working directory of the host system instead of letting Python decide. It is only possible to mount paths inside `/Users` when using boot2docker on OS X
* Minor code changes in relation to Pylint code check

## 1.0.0 - 2015-01-28
* Initial release
