# JS8CLI
### A JS8Call command line utility.

## Background
This simple utility is designed to facilitate updating JS8Call's location and to facilitate sending APRS SMS and grid location messages to spotters. This utiity can also be used to automatically update JS8Call's location as well as automatically send grid beaons to APRS-IS via spotters.

## Requirements
- Python 3 (Tested with Python 3.8)
- PIP installed
- GPSD installed and running
- JS8Call installed and running

## Setup
lksajflakjsdfljdsf

## How to use as a CLI utility
### To update JS8Call's grid square location based on GPS location:

`js8cli setgrid`

Optional arguments:

`--grid n` where n is the accuracy of the maidenhead grid squiare used: 1-5. Ex: 1 will give a maidenhead position of `AA`. Providing 2 will provide `AA11`, 4 will provide `AA11aa11`.

### To send your grid location to APRS via a spotter:

`js8cli aprsgrid`

Optional arguments:

`--grid n` where n is the accuracy of the maidenhead grid squiare used: 1-5. Ex: 1 will give a maidenhead position of `AA`. Providing 2 will provide `AA11`, 4 will provide `AA11aa11`.

`-d` prevents JS8Call from sending the message allowing the user to choose when to send it.

### To send an SMS via APRS using SMSGTE:

`js8cli aprssms --to 5555555555 --msg "Hello, world."`

Where `--to` specifies a phone number or [smsgte.org](https://smsgte.org) alias, and `--msg` is the message contnent or shortcut you wish to send.

Optional arguments:

`-d` prevents JS8Call from sending the message allowing the user to choose when to send it.

## Automatically updating JS8Call location and/or APRS grid location periodically.
This is accomplished by either exeuting `js8cli daemon` or by copying the systemd configuration file into place, enabling and starting it after configuring `aprs_loc_update_min` and `js8call_loc_refresh_min` in `js8cli.json`. These settings configure the timing of APRS location updates in minutes and the JS8Call location updates from the GPS in minutes as well.

After the configuration file has been modified the systemd unit can be copied into place and set up using the following commands:

```bash
sudo cp util/js8cli.service /etc/systemd/system
sudo systemctl enable js8cli
sudo systemctl start js8cli
```

```json
{
  "aprs_loc_update_min": 0,
  "gpsd_host": "127.0.0.1",
  "gpsd_port": 2947,
  "grid_level": 4,
  "js8call_host": "127.0.0.1",
  "js8call_loc_refresh_min": 5,
  "js8call_port": 2442,
  "js8call_proto": "tcp"
}
```