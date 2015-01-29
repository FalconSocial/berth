# Berth Changelog

## 1.0.1 - 2015-01-29
* Stop the package generation flow if the build script fails (exits with non-zero exit code)
* Disable hostname verification for Docker client, since the hostname and certificate doesn't match when using boot2docker - Fig does this as well
* Place the build script file in the current working directory of the host system instead of letting Python decide. It is only possible to mount paths inside `/Users` when using boot2docker on OS X
* Minor code changes in relation to Pylint code check

## 1.0.0 - 2015-01-28
* Initial release
