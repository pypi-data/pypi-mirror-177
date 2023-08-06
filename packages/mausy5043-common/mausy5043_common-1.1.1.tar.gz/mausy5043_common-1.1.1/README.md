# mausy5043-common

Provides various Python3 functions and classes for personal use.

## NOTE:
### user action required !!
Before trying to use the SQLITE3 functions in this package make sure you have installed the sqlite3 server/client and 
the default Python package that comes with it.

## Available commands for package building
`./build --build` builds the distribution files   
`./build --dist` uploads the distribution files to PyPi   
`./build --test` uploads the dictribution files to TestPyPi   
`./build --update` **discards all changes to the local copy** of the repo and pulls the current state of the repo from GitHub.

## Functions provided
`cat(filename)` : Read a file into a variable.   
`syslog_trace(trace, logerr, out2console)` : Log messages to console and/or system log.   
`moisture(temperature, relative_humidity, pressure)` : Calculate the moisture content of air given T [degC], RH [%] and P [hPa].   
`wet_bulb_temperature(temperature, relative_humidity)` : Calculate the wet bulb temperature of the air given T [degC] and RH [%].   

## Classes provided
`GracefulKiller` : A simple version of [this one](https://pypi.org/project/GracefulKiller/).   
`SqlDatabase` : A class to interact with SQLite3 databases.
