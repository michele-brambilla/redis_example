# psi_example.py #

Dummy program to fill,read,update and listen a redis database. A couple of example configurations are provided.

## Usage: ##

### Fill (populate) the database ###

```
python psi_example.py -p <config>
```

Read the configuration <config> provided as a jSON serialised structure and fill the database. Ideally opens a communication channel for each hash/set (TODO).

### Dump (query) the (whole) database ###

```
python psi_example.py -q
```

Print on the terminal the list of all the hash names, the available keys and their value. Sets are printed as well. Using

```
python psi_example.py -k <name>
```

Query the database for the hash or set named <name> and print on the screen.

### Listen for database changes ###

```
python psi_example.py -l <source list>
```

Listen the database for changes on all the sources in source list. Sources must be comma separated. The code subscribe to as many pubsub channels as sources in the list. Any change is notified and printed on the screen.

### Change (update) an entry in the database ###

```
python psi_example.py -u <hash name, key, new value>
```

Update the key <key> within the database hash <hash name> with the value <new value>. Moreover send a messave in the pubsub channel <hash name> nad data corresponding to the key name that has been modified.

### Fetch a configuration ###
A single configuration in a jSON-like format can be fetched Using
```
python psi_example.py -f <configuration name>
```
Configuration can be send on the corresponding channel (TODO)?

## Example ##

First populate the database
```
python psi_example.py -p sample.js
```

then you can listen for some source
```
python psi_example.py -l source:instrument1:motor1,source:instrument1:motor2,source:instrument1:motor3
```
In a new shell let's update the IOC address for the motor2
```
python psi_example.py -u source:instrument1:motor2,address,IOC:m3
```
The listener notifies:

> Change on hash source:instrument1:motor2 key: address

To shut down the listener just press a key.
To fetch a whole configuration
```
python psi_example.py -f instrument2
```
returns
> {'experiment': {'id': '1234', 'name': 'diffraction'},
 'sources': {'motor1': {'address': 'IOC:m3', 'type': 'ca-motor'},
             'motor2': {'address': 'IOC:m2', 'type': 'ca-motor'},
             'motor3': {'address': 'IOC:m3', 'type': 'ca-motor'},
             'motor4': {'address': 'IOC:m4', 'type': 'ca-motor'},
             'temp2': {'address': 'STC2', 'type': 'pv-temp'}},
 'user': {'email': 'user1@esss.se', 'institute': 'ESS', 'name': 'user1'}}

## TODO ##

- Sources and instrument addition should open new channels and notify.
- Add a new source to an existing item (instrument, server) and notify
- Remove a source or  item and notify
- ...
